import { prisma } from "@/lib/prisma";
import {
  createBookshelfSchema,
  updateBookshelfSchema,
  createShelfSchema,
  updateShelfSchema,
  placeBookSchema,
  type CreateBookshelfInput,
  type UpdateBookshelfInput,
  type CreateShelfInput,
  type PlaceBookInput,
} from "./schemas";
import { type Result, ok, err, notFound, forbidden, conflict, internalError } from "@/lib/errors";
import type { Bookshelf, Shelf, BookPlacement, Book, UserBook } from "@prisma/client";

export type ShelfWithPlacements = Shelf & {
  placements: (BookPlacement & { userBook: UserBook & { book: Book } })[];
};

export type BookshelfWithShelves = Bookshelf & {
  shelves: ShelfWithPlacements[];
};

// ---------------------------------------------------------------------------
// Bookshelf CRUD
// ---------------------------------------------------------------------------

export async function createBookshelf(
  userId: string,
  input: CreateBookshelfInput,
): Promise<Result<Bookshelf>> {
  const parsed = createBookshelfSchema.safeParse(input);
  if (!parsed.success) {
    return err({
      type: "VALIDATION_ERROR",
      message: "Invalid bookshelf data",
      issues: parsed.error.flatten().fieldErrors as Record<string, string[]>,
    });
  }

  try {
    const bookshelf = await prisma.bookshelf.create({
      data: { ...parsed.data, userId },
    });
    return ok(bookshelf);
  } catch {
    return err(internalError("Failed to create bookshelf"));
  }
}

export async function getUserBookshelves(
  userId: string,
): Promise<Result<(Bookshelf & { bookCount: number })[]>> {
  try {
    const bookshelves = await prisma.bookshelf.findMany({
      where: { userId },
      orderBy: { createdAt: "asc" },
      include: {
        shelves: {
          select: {
            placements: {
              where: { isPlaced: true },
              select: { id: true },
            },
          },
        },
      },
    });
    
    return ok(bookshelves.map((bs) => ({
      ...bs,
      bookCount: bs.shelves.reduce((sum, shelf) => sum + shelf.placements.length, 0),
      shelves: undefined as any, // Remove shelves from response
    })) as (Bookshelf & { bookCount: number })[]);
  } catch {
    return err(internalError("Failed to fetch bookshelves"));
  }
}

/**
 * Returns full bookshelf data including shelves and placed books in order.
 */
export async function getBookshelfById(
  userId: string,
  bookshelfId: string,
): Promise<Result<BookshelfWithShelves>> {
  try {
    const bookshelf = await prisma.bookshelf.findFirst({
      where: { id: bookshelfId, userId },
      include: {
        shelves: {
          orderBy: { order: "asc" },
          include: {
            placements: {
              where: { isPlaced: true },
              orderBy: { position: "asc" },
              include: {
                userBook: {
                  include: { book: true },
                },
              },
            },
          },
        },
      },
    });

    if (!bookshelf) return err(notFound("Bookshelf not found"));
    return ok(bookshelf);
  } catch {
    return err(internalError("Failed to fetch bookshelf"));
  }
}

export async function updateBookshelf(
  userId: string,
  bookshelfId: string,
  input: UpdateBookshelfInput,
): Promise<Result<Bookshelf>> {
  const parsed = updateBookshelfSchema.safeParse(input);
  if (!parsed.success) {
    return err({
      type: "VALIDATION_ERROR",
      message: "Invalid update data",
      issues: parsed.error.flatten().fieldErrors as Record<string, string[]>,
    });
  }

  try {
    const existing = await prisma.bookshelf.findFirst({ where: { id: bookshelfId, userId } });
    if (!existing) return err(notFound("Bookshelf not found"));

    const updated = await prisma.bookshelf.update({
      where: { id: bookshelfId },
      data: parsed.data,
    });
    return ok(updated);
  } catch {
    return err(internalError("Failed to update bookshelf"));
  }
}

export async function deleteBookshelf(
  userId: string,
  bookshelfId: string,
): Promise<Result<void>> {
  try {
    const existing = await prisma.bookshelf.findFirst({ where: { id: bookshelfId, userId } });
    if (!existing) return err(notFound("Bookshelf not found"));

    // Delete in transaction: bookplacements -> shelves -> bookshelf
    await prisma.$transaction(async (tx) => {
      // Get all shelves for this bookshelf
      const shelves = await tx.shelf.findMany({
        where: { bookshelfId },
        select: { id: true },
      });

      // Delete all book placements for all shelves
      for (const shelf of shelves) {
        await tx.bookPlacement.deleteMany({
          where: { shelfId: shelf.id },
        });
      }

      // Delete all shelves
      await tx.shelf.deleteMany({
        where: { bookshelfId },
      });

      // Delete the bookshelf
      await tx.bookshelf.delete({ where: { id: bookshelfId } });
    });

    return ok(undefined);
  } catch (error) {
    console.error("[deleteBookshelf] Error:", error);
    return err(internalError("Failed to delete bookshelf"));
  }
}

// ---------------------------------------------------------------------------
// Shelf (level) management
// ---------------------------------------------------------------------------

export async function addShelf(
  userId: string,
  input: CreateShelfInput,
): Promise<Result<Shelf>> {
  const parsed = createShelfSchema.safeParse(input);
  if (!parsed.success) {
    return err({
      type: "VALIDATION_ERROR",
      message: "Invalid shelf data",
      issues: parsed.error.flatten().fieldErrors as Record<string, string[]>,
    });
  }

  const { bookshelfId, ...shelfData } = parsed.data;

  const bookshelf = await prisma.bookshelf.findFirst({ where: { id: bookshelfId, userId } });
  if (!bookshelf) return err(forbidden("Bookshelf not accessible"));

  try {
    const shelf = await prisma.shelf.create({ data: { bookshelfId, ...shelfData } });
    return ok(shelf);
  } catch {
    return err(conflict("A shelf with this order already exists"));
  }
}

export async function updateShelfById(
  userId: string,
  shelfId: string,
  input: Partial<Omit<CreateShelfInput, "bookshelfId">>,
): Promise<Result<Shelf>> {
  const parsed = updateShelfSchema.safeParse(input);
  if (!parsed.success) {
    return err({
      type: "VALIDATION_ERROR",
      message: "Invalid shelf data",
      issues: parsed.error.flatten().fieldErrors as Record<string, string[]>,
    });
  }

  const shelf = await prisma.shelf.findFirst({
    where: { id: shelfId, bookshelf: { userId } },
  });
  if (!shelf) return err(notFound("Shelf not found"));

  try {
    const updated = await prisma.shelf.update({ where: { id: shelfId }, data: parsed.data });
    return ok(updated);
  } catch {
    return err(internalError("Failed to update shelf"));
  }
}

export async function deleteShelf(userId: string, shelfId: string): Promise<Result<void>> {
  const shelf = await prisma.shelf.findFirst({
    where: { id: shelfId, bookshelf: { userId } },
  });
  if (!shelf) return err(notFound("Shelf not found"));

  try {
    // Delete in transaction: first delete placements, then shelf
    await prisma.$transaction(async (tx) => {
      // Delete all book placements on this shelf
      await tx.bookPlacement.deleteMany({
        where: { shelfId },
      });

      // Then delete the shelf
      await tx.shelf.delete({ where: { id: shelfId } });
    });

    return ok(undefined);
  } catch {
    return err(internalError("Failed to delete shelf"));
  }
}

// ---------------------------------------------------------------------------
// Book placement
// ---------------------------------------------------------------------------

export async function placeBook(
  userId: string,
  input: PlaceBookInput,
): Promise<Result<BookPlacement>> {
  const parsed = placeBookSchema.safeParse(input);
  if (!parsed.success) {
    return err({
      type: "VALIDATION_ERROR",
      message: "Invalid placement data",
      issues: parsed.error.flatten().fieldErrors as Record<string, string[]>,
    });
  }

  const { userBookId, bookshelfId, shelfId, position, widthSpan } = parsed.data;

  // Verify ownership
  const userBook = await prisma.userBook.findFirst({ where: { id: userBookId, userId } });
  if (!userBook) return err(forbidden("Book not found in your collection"));

  const shelf = await prisma.shelf.findFirst({
    where: { id: shelfId, bookshelfId, bookshelf: { userId } },
  });
  if (!shelf) return err(notFound("Shelf not found on this bookshelf"));

  // Check if book is already placed (in any shelf)
  const existingPlacement = await prisma.bookPlacement.findFirst({
    where: { userBookId },
  });
  if (existingPlacement) {
    return err(conflict("Book is already placed on another shelf"));
  }

  try {
    const placement = await prisma.bookPlacement.create({
      data: { userBookId, bookshelfId, shelfId, position, widthSpan, isPlaced: true },
    });
    return ok(placement);
  } catch {
    return err(conflict("Position already occupied on this shelf"));
  }
}

export async function removeBookPlacement(
  userId: string,
  userBookId: string,
): Promise<Result<void>> {
  const userBook = await prisma.userBook.findFirst({ where: { id: userBookId, userId } });
  if (!userBook) return err(forbidden("Book not found in your collection"));

  await prisma.bookPlacement.deleteMany({ where: { userBookId } });
  return ok(undefined);
}

/**
 * Moves a book placement to a new shelf and/or position.
 * Accepts the placement's own id (not userBookId).
 * Reassigns positions on both the source and destination shelves so there
 * are no gaps or collisions.
 */
/**
 * Moves a book placement to a new shelf and/or position.
 * If swapWith is provided, swaps positions with another placement.
 * Accepts the placement's own id (not userBookId).
 */
export async function moveBookPlacement(
  userId: string,
  placementId: string,
  toShelfId: string,
  toPosition: number,
): Promise<Result<BookPlacement>> {
  console.log(`[moveBookPlacement] CALLED with:`, { placementId, toShelfId, toPosition });

  // Verify ownership via the placement → userBook → user chain
  const placement = await prisma.bookPlacement.findFirst({
    where: { id: placementId, userBook: { userId } },
    include: { userBook: true },
  });
  if (!placement) {
    console.log(`[moveBookPlacement] Placement not found`);
    return err(notFound("Placement not found"));
  }

  const targetShelf = await prisma.shelf.findFirst({
    where: { id: toShelfId, bookshelf: { userId } },
  });
  if (!targetShelf) return err(notFound("Target shelf not found"));

  try {
    // Check if target position is already occupied (if same shelf)
    if (placement.shelfId === toShelfId) {
      const existingAtPosition = await prisma.bookPlacement.findUnique({
        where: {
          shelfId_position: {
            shelfId: toShelfId,
            position: toPosition,
          },
        },
      });

      if (existingAtPosition && existingAtPosition.id !== placementId) {
        console.log(`[moveBookPlacement] Position ${toPosition} is already occupied, no change`);
        return ok(placement); // Return current placement unchanged
      }
    }

    // Move book to new shelf and position
    console.log(`[moveBookPlacement] Moving to shelf ${toShelfId}, position ${toPosition}`);

    const updated = await prisma.bookPlacement.update({
      where: { id: placementId },
      data: {
        shelfId: toShelfId,
        position: toPosition,
      },
    });

    console.log(`[moveBookPlacement] Successfully moved to position=${toPosition}`);
    return ok(updated);
  } catch (error) {
    console.error(`[moveBookPlacement] Error:`, error);
    return err(internalError("Failed to move book placement"));
  }
}
