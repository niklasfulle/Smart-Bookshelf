import Link from "next/link";
import { requireAuth } from "@/lib/auth-utils";
import { getUserBookshelves } from "@/features/bookshelves/service";
import { Card, CardContent } from "@/components/ui/Card";
import { getDict } from "@/lib/locale";
import { BookshelfCard } from "./BookshelfCard";

export default async function BookshelvesPage() {
  const session = await requireAuth();
  const [result, t] = await Promise.all([
    getUserBookshelves(session.user.id),
    getDict(),
  ]);
  const bookshelves = result.success ? result.data : [];

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">{t.bookshelves.title}</h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            {bookshelves.length} {bookshelves.length !== 1 ? t.bookshelves.shelves : t.bookshelves.shelf} {t.bookshelves.total}
          </p>
        </div>
        <Link
          href="/bookshelves/new"
          className="inline-flex items-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 transition-colors"
        >
          {t.bookshelves.newBookshelf}
        </Link>
      </div>

      {bookshelves.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center gap-4 py-16 text-center">
            <svg
              className="h-16 w-16 text-gray-200 dark:text-gray-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1}
                d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
              />
            </svg>
            <div>
              <p className="font-medium text-gray-900 dark:text-gray-100">{t.bookshelves.noShelvesYet}</p>
              <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                {t.bookshelves.noShelvesDesc}
              </p>
            </div>
            <Link
              href="/bookshelves/new"
              className="inline-flex items-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 transition-colors"
            >
              {t.bookshelves.createBookshelf}
            </Link>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {bookshelves.map((bs) => (
            <BookshelfCard key={bs.id} {...bs} />
          ))}
        </div>
      )}
    </div>
  );
}
