"use client";

import { useState, useTransition } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Card, CardContent } from "@/components/ui/Card";
import { useAppContext } from "@/contexts/AppContext";

interface BookshelfCardProps {
  id: string;
  name: string;
  description?: string | null;
  location?: string | null;
  bookCount: number;
  createdAt: Date;
}

export function BookshelfCard({
  id,
  name,
  description,
  location,
  bookCount,
  createdAt,
}: BookshelfCardProps) {
  const router = useRouter();
  const { t } = useAppContext();
  const [isPending, startTransition] = useTransition();
  const [showConfirm, setShowConfirm] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleDelete(e: React.MouseEvent) {
    e.preventDefault();
    e.stopPropagation();
    
    setError(null);
    startTransition(async () => {
      const res = await fetch(`/api/bookshelves/${id}`, {
        method: "DELETE",
      });

      if (!res.ok) {
        const json = await res.json() as { error?: string };
        setError(json.error ?? "Failed to delete bookshelf");
        return;
      }

      setShowConfirm(false);
      router.refresh();
    });
  }

  return (
    <>
      <Link href={`/bookshelves/${id}`}>
        <Card className="h-full transition-shadow hover:shadow-md relative">
          <CardContent>
            <div className="flex items-start justify-between gap-2">
              <div className="flex-1 min-w-0">
                <h2 className="font-semibold text-gray-900 dark:text-gray-100 break-words">{name}</h2>
                {description && (
                  <p className="mt-1 line-clamp-2 text-sm text-gray-500 dark:text-gray-400">{description}</p>
                )}
                {location && (
                  <p className="mt-2 text-xs text-gray-400 dark:text-gray-500">📍 {location}</p>
                )}
              </div>
              <button
                onClick={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  setShowConfirm(true);
                }}
                disabled={isPending}
                aria-label={t.bookshelves.remove}
                className="flex-shrink-0 flex h-6 w-6 items-center justify-center rounded text-gray-400 transition-colors hover:text-red-600 hover:bg-red-50 disabled:opacity-40 dark:hover:bg-red-900/30 dark:hover:text-red-400"
              >
                {isPending ? (
                  <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4l3-3-3-3v4a8 8 0 00-8 8h4z" />
                  </svg>
                ) : (
                  <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="3 6 5 6 21 6" />
                    <path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6" />
                    <path d="M10 11v6M14 11v6" />
                    <path d="M9 6V4a1 1 0 011-1h4a1 1 0 011 1v2" />
                  </svg>
                )}
              </button>
            </div>
            <div className="mt-3 space-y-1">
              <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
                {bookCount} {bookCount !== 1 ? t.bookshelves.books : t.bookshelves.book}
              </p>
              <p className="text-xs text-gray-400 dark:text-gray-500">
                {t.bookshelves.created} {new Date(createdAt).toLocaleDateString("de-DE", { year: "numeric", month: "2-digit", day: "2-digit" })}
              </p>
            </div>
          </CardContent>
        </Card>
      </Link>

      {showConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
          <div className="w-full max-w-sm rounded-xl bg-white p-6 shadow-2xl dark:bg-gray-900">
            {error && (
              <p className="mb-4 text-sm text-red-600 dark:text-red-400">{error}</p>
            )}
            <p className="text-sm text-gray-700 dark:text-gray-200">
              {t.bookshelves.confirmDeleteBookshelf}
            </p>
            <div className="mt-5 flex justify-end gap-2">
              <button
                onClick={() => setShowConfirm(false)}
                disabled={isPending}
                className="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-800"
              >
                {t.bookshelves.confirmDeleteCancel}
              </button>
              <button
                onClick={handleDelete}
                disabled={isPending}
                className="rounded-md bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700 transition-colors disabled:opacity-60"
              >
                {isPending ? t.bookshelves.removing : t.bookshelves.remove}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
