import Link from "next/link";
import Image from "next/image";
import { requireAuth } from "@/lib/auth-utils";
import { getUserBookshelves } from "@/features/bookshelves/service";
import { getUserBooks } from "@/features/books/service";
import { Card, CardContent } from "@/components/ui/Card";
import { getDict } from "@/lib/locale";

export default async function DashboardPage() {
  const session = await requireAuth();
  const userId = session.user.id;

  const [bookshelvesResult, booksResult, readBooksResult, t] = await Promise.all([
    getUserBookshelves(userId),
    getUserBooks(userId, { pageSize: 5 }),
    getUserBooks(userId, { status: "READ", pageSize: 5 }),
    getDict(),
  ]);

  const bookshelves = bookshelvesResult.success ? bookshelvesResult.data : [];
  const recentBooks = booksResult.success ? booksResult.data.items : [];
  const readBooks = readBooksResult.success ? readBooksResult.data : { items: [], total: 0 };
  const readBooksCount = readBooks.total || 0;
  const totalBooks = booksResult.success ? booksResult.data.total : 0;

  return (
    <div className="flex flex-col gap-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
          {t.dashboard.welcomeBack}{session.user.name ? `, ${session.user.name}` : ""}!
        </h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          {t.dashboard.subtitle}
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
        <Card>
          <CardContent>
            <p className="text-3xl font-bold text-indigo-600">{bookshelves.length}</p>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">{t.dashboard.statBookshelves}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <p className="text-3xl font-bold text-indigo-600">{totalBooks}</p>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">{t.dashboard.statBooks}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <p className="text-3xl font-bold text-indigo-600">{readBooksCount}</p>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">{t.dashboard.statReadBooks}</p>
          </CardContent>
        </Card>
      </div>

      {/* Bookshelves overview */}
      <section>
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">{t.dashboard.yourBookshelves}</h2>
          <Link
            href="/bookshelves"
            className="inline-flex items-center rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm font-medium text-gray-900 hover:bg-gray-50 transition-colors dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 dark:hover:bg-gray-700"
          >
            {t.dashboard.viewAll}
          </Link>
        </div>

        {bookshelves.length === 0 ? (
          <Card>
            <CardContent className="flex flex-col items-center gap-3 py-10 text-center">
              <p className="text-sm text-gray-500 dark:text-gray-400">{t.dashboard.noBookshelves}</p>
              <Link
                href="/bookshelves"
                className="inline-flex items-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-indigo-700 transition-colors"
              >
                {t.dashboard.createBookshelf}
              </Link>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {bookshelves.slice(0, 6).map((shelf) => (
              <Link key={shelf.id} href={`/bookshelves/${shelf.id}`}>
                <Card className="transition-shadow hover:shadow-md">
                  <CardContent>
                    <p className="font-semibold text-gray-900 dark:text-gray-100">{shelf.name}</p>
                    {shelf.description && (
                      <p className="mt-1 truncate text-sm text-gray-500 dark:text-gray-400">{shelf.description}</p>
                    )}
                    {shelf.location && (
                      <p className="mt-1 text-xs text-gray-400 dark:text-gray-500">📍 {shelf.location}</p>
                    )}
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        )}
      </section>

      {/* Recent books */}
      {recentBooks.length > 0 && (
        <section>
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">{t.dashboard.recentlyAdded}</h2>
            <Link href="/books" className="text-sm text-indigo-600 hover:text-indigo-500 dark:text-indigo-400">
              {t.dashboard.viewAllBooks}
            </Link>
          </div>
          <div className="flex flex-col gap-2">
            {recentBooks.map((ub) => (
              <div
                key={ub.id}
                className="flex items-center gap-3 rounded-lg border border-gray-200 bg-white p-3 dark:border-gray-700 dark:bg-gray-800"
              >
                <div
                  className="h-10 w-7 flex-shrink-0 rounded"
                  style={{ backgroundColor: ub.book.spineColor ?? "#e5e7eb" }}
                >
                  {ub.book.coverImageUrl ? (
                    <Image
                      src={ub.book.coverImageUrl}
                      alt={`Cover of ${ub.book.title}`}
                      width={28}
                      height={40}
                      className="h-full w-full object-cover"
                      unoptimized
                    />
                  ) : null}
                </div>
                <div className="min-w-0">
                  <p className="truncate text-sm font-medium text-gray-900 dark:text-gray-100">{ub.book.title}</p>
                  <p className="truncate text-xs text-gray-500 dark:text-gray-400">
                    {ub.book.authors.slice(0, 2).join(", ")}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
