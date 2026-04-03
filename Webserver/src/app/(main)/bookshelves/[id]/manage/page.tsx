import { notFound } from "next/navigation";
import Link from "next/link";
import { requireAuth } from "@/lib/auth-utils";
import { getBookshelfById } from "@/features/bookshelves/service";
import { Card, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { getDict } from "@/lib/locale";
import { EditBookshelfInline, AddShelfForm, DeleteShelfButton } from "./ManageActions";

interface ManageBookshelfPageProps {
  params: Promise<{ id: string }>;
}

export default async function ManageBookshelfPage({ params }: ManageBookshelfPageProps) {
  const session = await requireAuth();
  const { id } = await params;
  const [result, t] = await Promise.all([
    getBookshelfById(session.user.id, id),
    getDict(),
  ]);

  if (!result.success) notFound();

  const bookshelf = result.data;
  const sortedShelves = [...bookshelf.shelves].sort((a, b) => a.order - b.order);
  const nextOrder = (bookshelf.shelves.reduce((max, s) => Math.max(max, s.order), 0)) + 1;

  return (
    <div className="mx-auto max-w-2xl flex flex-col gap-6">
      <div>
        <Link
          href={`/bookshelves/${id}`}
          className="text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
        >
          ← {bookshelf.name}
        </Link>
        <h1 className="mt-2 text-2xl font-bold text-gray-900 dark:text-gray-100">
          {t.bookshelves.manageTitle}
        </h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          {t.bookshelves.manageSubtitle}
        </p>
      </div>

      {/* ── Details ── */}
      <Card>
        <CardContent>
          <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-gray-600 dark:text-gray-400">
            {t.bookshelves.detailsSection}
          </h2>
          <EditBookshelfInline
            bookshelfId={id}
            initialName={bookshelf.name}
            initialDescription={bookshelf.description}
            initialLocation={bookshelf.location}
          />
        </CardContent>
      </Card>

      {/* ── Add shelf level ── */}
      <Card>
        <CardContent>
          <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-gray-600 dark:text-gray-400">
            {t.bookshelves.shelfLevelsSection}
          </h2>
          <AddShelfForm bookshelfId={id} nextOrder={nextOrder} />
        </CardContent>
      </Card>

      {/* ── Current shelf levels ── */}
      {sortedShelves.length > 0 ? (
        <div className="flex flex-col gap-3">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-gray-600 dark:text-gray-400">
            {t.bookshelves.currentLevels} ({sortedShelves.length})
          </h2>
          {sortedShelves.map((shelf) => {
            const calculatedZones = Math.max(1, Math.floor((shelf.widthCm || 80) / 3.5));
            return (
              <div
                key={shelf.id}
                className="flex items-center justify-between rounded-lg border border-gray-200 bg-white px-4 py-3 dark:border-gray-700 dark:bg-gray-800"
              >
                <div className="flex items-center gap-3">
                  <span className="flex h-7 w-7 items-center justify-center rounded-full bg-gray-100 text-xs font-bold text-gray-600 dark:bg-gray-700 dark:text-gray-300">
                    {shelf.order}
                  </span>
                  <div>
                    <span className="font-medium text-gray-800 dark:text-gray-100">
                      {shelf.name ?? `${t.bookshelves.shelfLabel} ${shelf.order}`}
                    </span>
                    {shelf.widthCm && (
                      <span className="ml-2 text-xs text-gray-400">{shelf.widthCm} cm</span>
                    )}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="gray">
                    {shelf.placements.length} {shelf.placements.length !== 1 ? t.books.books : t.books.book}
                  </Badge>
                  <Badge variant="gray">
                    {calculatedZones} {calculatedZones === 1 ? 'zone' : 'zones'}
                  </Badge>
                  <DeleteShelfButton shelfId={shelf.id} />
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <p className="text-sm text-gray-500 dark:text-gray-400">{t.bookshelves.noLevels}</p>
      )}
    </div>
  );
}
