/**
 * Book import service – abstracts external metadata lookup behind a clean interface.
 *
 * Currently implements Open Library lookup as the primary source.
 * Additional providers (Google Books, etc.) can be added here without
 * touching UI or the book service.
 */
import type { CreateBookInput } from "./schemas";

export interface BookMetadata {
  isbn?: string;
  title: string;
  subtitle?: string;
  authors: string[];
  publisher?: string;
  publishedYear?: number;
  coverImageUrl?: string;
  pageCount?: number;
  language?: string;
}

/**
 * Fetches book metadata from Open Library by ISBN.
 * Returns null if no match is found or the request fails.
 */
export async function fetchBookMetadataByIsbn(isbn: string): Promise<BookMetadata | null> {
  const cleanIsbn = isbn.replaceAll(/[-\s]/g, "");

  try {
    const res = await fetch(
      `https://openlibrary.org/api/books?bibkeys=ISBN:${cleanIsbn}&format=json&jscmd=data`,
      { next: { revalidate: 86400 } }, // cache for 24 hours
    );

    if (!res.ok) return null;

    const data = await res.json() as Record<string, OpenLibraryBook>;
    const key = `ISBN:${cleanIsbn}`;
    const book = data[key];
    if (!book) return null;

    return mapOpenLibraryToMetadata(cleanIsbn, book);
  } catch {
    // Treat lookup failures as a normal business case, not a system error.
    return null;
  }
}

/**
 * Fetches book metadata from Open Library by barcode (EAN-13 / UPC).
 * Many barcodes on books are the ISBN-13, so we try that first.
 */
export async function fetchBookMetadataByBarcode(barcode: string): Promise<BookMetadata | null> {
  // Most book barcodes encode the ISBN-13 directly.
  return fetchBookMetadataByIsbn(barcode);
}

// ---------------------------------------------------------------------------
// Converts a CreateBookInput from the form with prefilled/overridden metadata
// ---------------------------------------------------------------------------

export function mergeMetadataWithInput(
  metadata: BookMetadata,
  partial: Partial<CreateBookInput> = {},
): CreateBookInput {
  return {
    isbn: partial.isbn ?? metadata.isbn,
    title: partial.title ?? metadata.title,
    subtitle: partial.subtitle ?? metadata.subtitle,
    authors: partial.authors ?? metadata.authors,
    publisher: partial.publisher ?? metadata.publisher,
    publishedYear: partial.publishedYear ?? metadata.publishedYear,
    coverImageUrl: partial.coverImageUrl ?? metadata.coverImageUrl,
    pageCount: partial.pageCount ?? metadata.pageCount,
    language: partial.language ?? metadata.language,
    spineColor: partial.spineColor,
    widthCm: partial.widthCm,
    heightCm: partial.heightCm,
    thicknessCm: partial.thicknessCm,
  };
}

// ---------------------------------------------------------------------------
// Open Library response shape (minimal subset we use)
// ---------------------------------------------------------------------------

interface OpenLibraryBook {
  title?: string;
  subtitle?: string;
  authors?: { name: string }[];
  publishers?: { name: string }[];
  publish_date?: string;
  cover?: { medium?: string; large?: string };
  number_of_pages?: number;
  languages?: { key: string }[];
  identifiers?: { isbn_13?: string[]; isbn_10?: string[] };
}

function mapOpenLibraryToMetadata(isbn: string, raw: OpenLibraryBook): BookMetadata {
  const publishedYear = raw.publish_date
    ? Number.parseInt(raw.publish_date.slice(-4), 10) || undefined
    : undefined;

  const language = raw.languages?.[0]?.key?.replaceAll("/languages/", "");

  return {
    isbn,
    title: raw.title ?? "Unknown Title",
    subtitle: raw.subtitle,
    authors: raw.authors?.map((a) => a.name) ?? [],
    publisher: raw.publishers?.[0]?.name,
    publishedYear: Number.isNaN(publishedYear) ? undefined : publishedYear,
    coverImageUrl: raw.cover?.large ?? raw.cover?.medium,
    pageCount: raw.number_of_pages,
    language,
  };
}
