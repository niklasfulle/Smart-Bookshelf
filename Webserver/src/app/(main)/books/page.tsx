import { requireAuth } from "@/lib/auth-utils";
import { getUserBooks } from "@/features/books/service";
import { BookCard } from "@/components/books/BookCard";
import { Button } from "@/components/ui/Button";
import { getDict } from "@/lib/locale";
import { AddBookButton } from "./AddBookButton";
import type { CollectionStatus } from "@prisma/client";

interface BooksPageProps {
  searchParams: Promise<{ q?: string; status?: string }>;
}

const allStatuses: CollectionStatus[] = ["OWNED", "READING", "READ", "WISHLIST", "LENT_OUT"];
const statusKeys: Record<CollectionStatus, keyof typeof import("@/lib/translations").translations["en"]["books"]> = {
  OWNED: "statusOwned",
  READING: "statusReading",
  READ: "statusRead",
  WISHLIST: "statusWishlist",
  LENT_OUT: "statusLentOut",
} as any;

export default async function BooksPage({ searchParams }: BooksPageProps) {
  const session = await requireAuth();
  const [resolvedParams, t] = await Promise.all([searchParams, getDict()]);

  const status = (allStatuses.includes(resolvedParams.status as CollectionStatus)
    ? resolvedParams.status
    : undefined) as CollectionStatus | undefined;

  const result = await getUserBooks(session.user.id, {
    search: resolvedParams.q,
    status,
    pageSize: 100,
  });

  const books = result.success ? result.data.items : [];
  const total = result.success ? result.data.total : 0;

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">{t.books.title}</h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            {total} {total !== 1 ? t.books.books : t.books.book} {t.books.inCollection}
          </p>
        </div>
        <AddBookButton />
      </div>

      {/* Search */}
      <form method="GET" className="flex gap-2">
        <input
          name="q"
          defaultValue={resolvedParams.q}
          placeholder={t.books.searchPlaceholder}
          className="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 dark:placeholder:text-gray-500"
        />
        <Button type="submit" variant="secondary">
          {t.books.search}
        </Button>
      </form>

      {/* Status Filter */}
      <div className="flex flex-wrap gap-2">
        <a
          href="/books"
          className={`rounded-md px-3 py-1.5 text-sm font-medium transition-colors ${
            !status
              ? "bg-indigo-600 text-white"
              : "border border-gray-300 bg-white text-gray-900 hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 dark:hover:bg-gray-700"
          }`}
        >
          {t.books.all || "All"}
        </a>
        {allStatuses.map((s) => (
          <a
            key={s}
            href={`/books?status=${s}${resolvedParams.q ? `&q=${resolvedParams.q}` : ""}`}
            className={`rounded-md px-3 py-1.5 text-sm font-medium transition-colors ${
              status === s
                ? "bg-indigo-600 text-white"
                : "border border-gray-300 bg-white text-gray-900 hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 dark:hover:bg-gray-700"
            }`}
          >
            {t.books[statusKeys[s]]}
          </a>
        ))}
      </div>

      {books.length === 0 ? (
        <div className="flex flex-col items-center gap-3 py-16 text-center">
          <p className="font-medium text-gray-700 dark:text-gray-300">{t.books.noBooksFound}</p>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            {resolvedParams.q
              ? `${t.books.noResults} "${resolvedParams.q}"`
              : t.books.addFirst}
          </p>
        </div>
      ) : (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {books.map((ub) => (
            <BookCard
              key={ub.id}
              userBook={ub}
              isPlaced={false}
            />
          ))}
        </div>
      )}
    </div>
  );
}

