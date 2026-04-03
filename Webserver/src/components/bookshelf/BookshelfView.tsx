import { ShelfLevel } from "./ShelfLevel";
import type { BookshelfWithShelves } from "@/features/bookshelves/service";

interface BookshelfViewProps {
  bookshelf: BookshelfWithShelves;
  shelfLabel: string;
  noBooks: string;
  noShelvesVisual: string;
}

/**
 * Full visual bookshelf renderer.
 *
 * Displays all shelf levels stacked vertically (top shelf = highest order).
 * Each shelf renders its books as clickable spine blocks.
 */
export function BookshelfView({ bookshelf, shelfLabel, noBooks, noShelvesVisual }: BookshelfViewProps) {
  if (bookshelf.shelves.length === 0) {
    return (
      <div className="flex min-h-[200px] w-full flex-col items-center justify-center gap-3 rounded-lg border-2 border-dashed border-gray-200 p-8 text-center dark:border-gray-700">
        <svg
          className="h-12 w-12 text-gray-300"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25"
          />
        </svg>
        <p className="text-sm text-gray-500 dark:text-gray-400">{noShelvesVisual}</p>
      </div>
    );
  }

  // Display shelves top-to-bottom: lowest order first (shelf 1 is on top visually)
  const orderedShelves = [...bookshelf.shelves].sort((a, b) => a.order - b.order);

  return (
    <div
      className="w-full overflow-x-auto rounded-xl border border-gray-200 bg-amber-50 p-6 shadow-inner dark:border-gray-700 dark:bg-amber-950/20"
      aria-label={`Visual view of ${bookshelf.name}`}
    >
      <div className="flex min-w-max flex-col gap-2">
        {orderedShelves.map((shelf) => (
          <ShelfLevel key={shelf.id} shelf={shelf} shelfLabel={shelfLabel} noBooks={noBooks} />
        ))}
      </div>
    </div>
  );
}
