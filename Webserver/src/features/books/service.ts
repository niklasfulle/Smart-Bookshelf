import { prisma } from "@/lib/prisma";
import { createBookSchema, type CreateBookInput } from "./schemas";
import { type Result, ok, err, conflict, notFound, internalError } from "@/lib/errors";
import { extractCoverColor } from "@/lib/cover-color";
import type { Book, UserBook, CollectionStatus } from "@prisma/client";

export type UserBookWithBook = UserBook & { book: Book };

// ---------------------------------------------------------------------------
// Book upsert (canonical record – shared across users)
// ---------------------------------------------------------------------------

/**
 * Finds or creates a canonical Book record, then adds it to the user's collection.
 * If the user already owns this book, returns a CONFLICT error.
 */
export async function addBookToCollection(
  userId: string,
  input: CreateBookInput,
): Promise<Result<UserBookWithBook>> {
  const parsed = createBookSchema.safeParse(input);
  if (!parsed.success) {
    return err({
      type: "VALIDATION_ERROR",
      message: "Invalid book data",
      issues: parsed.error.flatten().fieldErrors as Record<string, string[]>,
    });
  }

  const { isbn, barcode, ...rest } = parsed.data;

  try {
    // Find or create the canonical book record.
    let book = isbn
      ? await prisma.book.findUnique({ where: { isbn } })
      : barcode
        ? await prisma.book.findUnique({ where: { barcode } })
        : null;

    if (!book) {
      // Auto-derive spine color from cover image when not explicitly provided.
      let spineColor = rest.spineColor;
      if (!spineColor && rest.coverImageUrl) {
        spineColor = (await extractCoverColor(rest.coverImageUrl)) ?? undefined;
      }
      book = await prisma.book.create({
        data: {
          isbn,
          barcode,
          ...rest,
          spineColor,
          metadataSource: "manual",
        },
      });
    }

    // Check if user already has this book.
    const existing = await prisma.userBook.findUnique({
      where: { userId_bookId: { userId, bookId: book.id } },
    });
    if (existing) {
      return err(conflict("This book is already in your collection"));
    }

    const userBook = await prisma.userBook.create({
      data: { userId, bookId: book.id },
      include: { book: true },
    });

    return ok(userBook);
  } catch {
    return err(internalError("Failed to add book to collection"));
  }
}

/**
 * Returns all books in the user's collection with placement info.
 */
export async function getUserBooks(
  userId: string,
  options: {
    search?: string;
    status?: CollectionStatus;
    page?: number;
    pageSize?: number;
    onlyUnplaced?: boolean;
  } = {},
): Promise<Result<{ items: UserBookWithBook[]; total: number }>> {
  const { search, status, page = 1, pageSize = 50, onlyUnplaced = false } = options;

  try {
    const where = {
      userId,
      ...(status ? { status } : {}),
      ...(onlyUnplaced ? { placement: null } : {}),
      ...(search
        ? {
            book: {
              OR: [
                { title: { contains: search, mode: "insensitive" as const } },
                { authors: { has: search } },
                { isbn: { contains: search } },
              ],
            },
          }
        : {}),
    };

    const [items, total] = await Promise.all([
      prisma.userBook.findMany({
        where,
        include: { book: true },
        orderBy: { createdAt: "desc" },
        skip: (page - 1) * pageSize,
        take: pageSize,
      }),
      prisma.userBook.count({ where }),
    ]);

    return ok({ items, total });
  } catch {
    return err(internalError("Failed to fetch collection"));
  }
}

/**
 * Removes a book from the user's collection (and its placement, if any).
 */
export async function removeBookFromCollection(
  userId: string,
  userBookId: string,
): Promise<Result<void>> {
  try {
    const userBook = await prisma.userBook.findFirst({
      where: { id: userBookId, userId },
    });

    if (!userBook) {
      return err(notFound("Book not found in your collection"));
    }

    await prisma.userBook.delete({ where: { id: userBookId } });
    return ok(undefined);
  } catch {
    return err(internalError("Failed to remove book"));
  }
}

/**
 * Updates collection status or notes for a user's book.
 */
export async function updateUserBook(
  userId: string,
  userBookId: string,
  data: { status?: CollectionStatus; notes?: string },
): Promise<Result<UserBookWithBook>> {
  try {
    const userBook = await prisma.userBook.findFirst({
      where: { id: userBookId, userId },
    });

    if (!userBook) {
      return err(notFound("Book not found in your collection"));
    }

    const updated = await prisma.userBook.update({
      where: { id: userBookId },
      data,
      include: { book: true },
    });

    return ok(updated);
  } catch {
    return err(internalError("Failed to update book"));
  }
}

/**
 * Updates the canonical Book record's metadata (title, cover, spine color, etc.)
 * Only allowed when the caller owns at least one UserBook referencing this Book.
 */
export async function updateBookDetails(
  userId: string,
  userBookId: string,
  data: {
    title?: string;
    subtitle?: string;
    authors?: string[];
    coverImageUrl?: string | null;
    spineColor?: string | null;
    publisher?: string;
    publishedYear?: number;
  },
): Promise<Result<Book>> {
  try {
    const userBook = await prisma.userBook.findFirst({
      where: { id: userBookId, userId },
    });
    if (!userBook) return err(notFound("Book not found in your collection"));

    // Always re-derive spine color from the effective cover URL.
    const mergedData = { ...data };
    const effectiveCoverUrl =
      "coverImageUrl" in data ? data.coverImageUrl : (await prisma.book.findUnique({ where: { id: userBook.bookId }, select: { coverImageUrl: true } }))?.coverImageUrl;
    if (effectiveCoverUrl) {
      const derived = await extractCoverColor(effectiveCoverUrl);
      if (derived) mergedData.spineColor = derived;
    }

    const updated = await prisma.book.update({
      where: { id: userBook.bookId },
      data: mergedData,
    });
    return ok(updated);
  } catch {
    return err(internalError("Failed to update book details"));
  }
}
