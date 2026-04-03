import { BookSpine } from "./BookSpine";
import type { ShelfWithPlacements } from "@/features/bookshelves/service";

interface ShelfLevelProps {
  shelf: ShelfWithPlacements;
  shelfLabel: string;
  noBooks: string;
}

const SHELF_HEIGHT_PX = 180; // total row height including board
const BOARD_HEIGHT_PX = 12;

/**
 * Renders a single shelf level as a horizontal row with:
 * - Book spines placed left-to-right in position order
 * - A visualized shelf board at the bottom
 * - Empty space markers for vacant positions
 */
export function ShelfLevel({ shelf, shelfLabel, noBooks }: ShelfLevelProps) {
  const label = shelf.name ?? `${shelfLabel} ${shelf.order}`;

  return (
    <div className="flex flex-col">
      {/* Shelf label */}
      <div className="mb-1 flex items-center gap-2">
        <span className="text-xs font-medium text-gray-400 dark:text-gray-500">{label}</span>
      </div>

      {/* Books standing on the shelf */}
      <div
        className="relative w-full overflow-x-clip overflow-y-visible"
        style={{ height: SHELF_HEIGHT_PX }}
      >
        {/* Book row */}
        <div
          className="absolute bottom-[var(--board)] flex items-end gap-0"
          style={{ "--board": `${BOARD_HEIGHT_PX}px` } as React.CSSProperties}
        >
          {shelf.placements.length === 0 ? (
            <div className="flex h-32 w-64 items-center justify-center rounded border-2 border-dashed border-gray-200 text-sm text-gray-400 dark:border-gray-600 dark:text-gray-500">
              {noBooks}
            </div>
          ) : (
            shelf.placements.map((placement) => {
              const { book } = placement.userBook;
              return (
                <BookSpine
                  key={placement.id}
                  title={book.title}
                  authors={book.authors}
                  spineColor={book.spineColor}
                  coverImageUrl={book.coverImageUrl}
                  thicknessCm={book.thicknessCm}
                  heightCm={book.heightCm}
                />
              );
            })
          )}
        </div>

        {/* Shelf board */}
        <div
          className="absolute right-0 bottom-0 left-0 rounded-sm"
          style={{
            height: BOARD_HEIGHT_PX,
            background:
              "linear-gradient(to bottom, #c8a96e 0%, #b08040 40%, #8b5e20 100%)",
            boxShadow: "0 2px 4px rgba(0,0,0,0.25)",
          }}
        />
      </div>
    </div>
  );
}
