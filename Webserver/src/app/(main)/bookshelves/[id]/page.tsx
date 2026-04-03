import { notFound } from "next/navigation";
import Link from "next/link";
import { requireAuth } from "@/lib/auth-utils";
import { getBookshelfById } from "@/features/bookshelves/service";
import { BookshelfDnd } from "@/components/bookshelf/BookshelfDnd";
import { Badge } from "@/components/ui/Badge";
import { getDict } from "@/lib/locale";
import { AddBookButton } from "./AddBookButton";

interface BookshelfDetailPageProps {
  params: Promise<{ id: string }>;
}

export default async function BookshelfDetailPage({ params }: BookshelfDetailPageProps) {
  const session = await requireAuth();
  const { id } = await params;
  const [result, t] = await Promise.all([
    getBookshelfById(session.user.id, id),
    getDict(),
  ]);

  if (!result.success) {
    notFound();
  }

  const bookshelf = result.data;
  const totalShelves = bookshelf.shelves.length;
  const totalPlacedBooks = bookshelf.shelves.reduce(
    (sum, shelf) => sum + shelf.placements.length,
    0,
  );

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <div className="flex items-center gap-3">
            <Link href="/bookshelves" className="text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
              ← {t.bookshelves.title}
            </Link>
          </div>
          <h1 className="mt-2 text-2xl font-bold text-gray-900 dark:text-gray-100">{bookshelf.name}</h1>
          {bookshelf.description && (
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">{bookshelf.description}</p>
          )}
          {bookshelf.location && (
            <p className="mt-1 text-xs text-gray-400 dark:text-gray-500">📍 {bookshelf.location}</p>
          )}
          <div className="mt-3 flex flex-wrap gap-2">
            <Badge variant="gray">{totalShelves} {totalShelves !== 1 ? t.bookshelves.shelves : t.bookshelves.shelf}</Badge>
            <Badge variant="indigo">{totalPlacedBooks} {totalPlacedBooks !== 1 ? t.books.books : t.books.book} {t.bookshelves.placed}</Badge>
          </div>
        </div>
        <div className="flex gap-2">
          <AddBookButton bookshelfId={bookshelf.id} shelves={bookshelf.shelves} />
          <Link
            href={`/bookshelves/${bookshelf.id}/manage`}
            className="inline-flex items-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-indigo-700 transition-colors"
          >
            {t.bookshelves.manageShelf}
          </Link>
        </div>
      </div>

      {/* Visual bookshelf */}
      <section>
        <h2 className="mb-3 text-sm font-semibold text-gray-700 uppercase tracking-wide dark:text-gray-400">
          {t.bookshelves.visualView}
        </h2>
        <BookshelfDnd bookshelf={bookshelf} shelfLabel={t.bookshelves.shelfLabel} noBooks={t.bookshelves.noBooks} noShelvesVisual={t.bookshelves.noShelvesVisual} />
      </section>

      {/* Shelf levels list */}
      {bookshelf.shelves.length > 0 && (
        <section>
          <h2 className="mb-3 text-sm font-semibold text-gray-700 uppercase tracking-wide dark:text-gray-400">
            {t.bookshelves.shelfLevels}
          </h2>
          <div className="flex flex-col gap-2">
            {[...bookshelf.shelves]
              .sort((a, b) => a.order - b.order)
              .map((shelf) => (
                <div
                  key={shelf.id}
                  className="flex items-center justify-between rounded-lg border border-gray-200 bg-white px-4 py-3 dark:border-gray-700 dark:bg-gray-800"
                >
                  <div>
                    <span className="font-medium text-gray-800 dark:text-gray-100">
                      {shelf.name ?? `${t.bookshelves.shelf} ${shelf.order}`}
                    </span>
                    {shelf.widthCm && (
                      <span className="ml-2 text-xs text-gray-400">{shelf.widthCm} {t.bookshelves.widthUnit}</span>
                    )}
                  </div>
                  <Badge variant="gray">
                    {shelf.placements.length} {shelf.placements.length !== 1 ? t.books.books : t.books.book}
                  </Badge>
                </div>
              ))}
          </div>
        </section>
      )}
    </div>
  );
}
