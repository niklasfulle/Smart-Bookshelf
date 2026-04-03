"use client";

import Image from "next/image";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { Badge } from "@/components/ui/Badge";
import { useAppContext } from "@/contexts/AppContext";
import type { UserBook, Book, CollectionStatus } from "@prisma/client";

const statusVariants: Record<CollectionStatus, "gray" | "green" | "yellow" | "blue" | "indigo" | "red"> = {
  OWNED: "yellow",
  READING: "blue",
  READ: "indigo",
  WISHLIST: "gray",
  LENT_OUT: "orange" as any,
};

const statusKeys: Record<CollectionStatus, keyof typeof import("@/lib/translations").translations["en"]["books"]> = {
  OWNED: "statusOwned",
  READING: "statusReading",
  READ: "statusRead",
  WISHLIST: "statusWishlist",
  LENT_OUT: "statusLentOut",
} as any;

const allStatuses: CollectionStatus[] = ["OWNED", "READING", "READ", "WISHLIST", "LENT_OUT"];

interface BookCardProps {
  userBook: UserBook & { book: Book };
  showPlacedStatus?: boolean;
  isPlaced?: boolean;
}

function EditBookModal({
  userBook,
  onClose,
}: Readonly<{
  userBook: UserBook & { book: Book };
  onClose: () => void;
}>) {
  const { t } = useAppContext();
  const b = t.books;
  const router = useRouter();
  const { book } = userBook;

  const [title, setTitle] = useState(book.title);
  const [subtitle, setSubtitle] = useState(book.subtitle ?? "");
  const [authors, setAuthors] = useState(book.authors.join(", "));
  const [coverUrl, setCoverUrl] = useState(book.coverImageUrl ?? "");
  const [spineColor, setSpineColor] = useState(book.spineColor ?? "#6366f1");
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSave() {
    setSaving(true);
    setError(null);
    try {
      const res = await fetch(`/api/books/${userBook.id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: title.trim() || undefined,
          subtitle: subtitle.trim() || undefined,
          authors: authors.split(",").map((a) => a.trim()).filter(Boolean),
          coverImageUrl: coverUrl.trim() || null,
          spineColor: spineColor.trim() || null,
        }),
      });
      if (!res.ok) {
        const data = await res.json();
        setError(data.error ?? "Error");
        return;
      }
      setSaved(true);
      router.refresh();
      setTimeout(onClose, 800);
    } finally {
      setSaving(false);
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      onClick={onClose}
    >
      <div
        className="w-full max-w-md rounded-lg bg-white p-6 shadow-xl dark:bg-gray-800"
        onClick={(e) => e.stopPropagation()}
      >
        <h2 className="mb-4 text-lg font-semibold text-gray-900 dark:text-gray-100">
          {b.editBookTitle}
        </h2>

        <div className="space-y-3">
          <label className="block">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-200">{b.titleLabel}</span>
            <input
              className="mt-1 w-full rounded border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </label>

          <label className="block">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-200">{b.subtitleLabel}</span>
            <input
              className="mt-1 w-full rounded border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100"
              value={subtitle}
              onChange={(e) => setSubtitle(e.target.value)}
            />
          </label>

          <label className="block">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-200">{b.authorsLabel}</span>
            <input
              className="mt-1 w-full rounded border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100"
              value={authors}
              onChange={(e) => setAuthors(e.target.value)}
            />
          </label>

          <label className="block">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-200">{b.coverUrlLabel}</span>
            <input
              className="mt-1 w-full rounded border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100"
              placeholder="https://…"
              value={coverUrl}
              onChange={(e) => setCoverUrl(e.target.value)}
            />
          </label>

          <label className="block">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-200">{b.spineColorLabel}</span>
            <div className="mt-1 flex items-center gap-2">
              <input
                type="color"
                className="h-9 w-10 cursor-pointer rounded border border-gray-300 p-0.5 dark:border-gray-600"
                value={spineColor}
                onChange={(e) => setSpineColor(e.target.value)}
              />
              <input
                className="flex-1 rounded border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100"
                value={spineColor}
                onChange={(e) => setSpineColor(e.target.value)}
              />
            </div>
          </label>
        </div>

        {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
        {saved && <p className="mt-3 text-sm text-green-600">{b.bookSaved}</p>}

        <div className="mt-5 flex justify-end gap-3">
          <button
            onClick={onClose}
            className="rounded px-4 py-2 text-sm text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700"
          >
            {t.bookshelves.cancelAdd}
          </button>
          <button
            onClick={handleSave}
            disabled={saving}
            className="rounded bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
          >
            {saving ? "…" : b.saveBook}
          </button>
        </div>
      </div>
    </div>
  );
}

export function BookCard({ userBook, showPlacedStatus = false, isPlaced = false }: Readonly<BookCardProps>) {
  const { t } = useAppContext();
  const router = useRouter();
  const { book } = userBook;
  const authorDisplay = book.authors.slice(0, 2).join(", ");
  const [editing, setEditing] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const statusLabel = t.books[statusKeys[userBook.status]] as string;
  const statusVariant = statusVariants[userBook.status];
  const [showStatusMenu, setShowStatusMenu] = useState(false);
  const [updatingStatus, setUpdatingStatus] = useState(false);

  async function handleStatusChange(newStatus: CollectionStatus) {
    if (newStatus === userBook.status) {
      setShowStatusMenu(false);
      return;
    }
    setUpdatingStatus(true);
    try {
      await fetch(`/api/books/${userBook.id}/status`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus }),
      });
      router.refresh();
    } finally {
      setUpdatingStatus(false);
      setShowStatusMenu(false);
    }
  }

  async function handleDelete() {
    setDeleting(true);
    await fetch(`/api/books/${userBook.id}`, { method: "DELETE" });
    router.refresh();
  }

  return (
    <>
      <article 
        className="group relative flex gap-4 rounded-lg border border-gray-200 bg-white p-4 shadow-sm transition-shadow hover:shadow-md dark:border-gray-700 dark:bg-gray-800"
        onClick={() => showStatusMenu && setShowStatusMenu(false)}
      >
        {/* Cover / color swatch */}
        <div
          className="flex h-24 w-16 flex-shrink-0 overflow-hidden rounded"
          style={{ backgroundColor: book.spineColor ?? "#e5e7eb" }}
        >
          {book.coverImageUrl ? (
            <Image
              src={book.coverImageUrl}
              alt={`Cover of ${book.title}`}
              width={64}
              height={96}
              className="h-full w-full object-cover"
              unoptimized
            />
          ) : (
            <div className="flex h-full w-full items-center justify-center">
              <span
                className="rotate-[-90deg] whitespace-nowrap text-[8px] font-semibold text-white/80"
                style={{ maxWidth: 88 }}
              ></span>
            </div>
          )}
        </div>

        {/* Metadata */}
        <div className="flex min-w-0 flex-1 flex-col gap-1">
          <div className="flex items-start justify-between gap-2">
            <h3 className="truncate text-sm font-semibold text-gray-900  dark:text-gray-100">
              {book.title}
            </h3>
            <div className="relative">
              <button
                onClick={() => setShowStatusMenu(!showStatusMenu)}
                disabled={updatingStatus}
                className="whitespace-nowrap"
              >
                <Badge variant={statusVariant}>{statusLabel}</Badge>
              </button>
              {showStatusMenu && (
                <div className="absolute right-0 top-full z-40 mt-1 flex flex-col rounded-lg border border-gray-300 bg-white shadow-lg dark:border-gray-600 dark:bg-gray-700">
                  {allStatuses.map((status) => (
                    <button
                      key={status}
                      onClick={() => handleStatusChange(status)}
                      className={`px-3 py-2 text-sm text-left hover:bg-gray-100 dark:hover:bg-gray-600 ${status === userBook.status ? "font-semibold" : ""}`}
                    >
                      {t.books[statusKeys[status]] as string}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          {book.subtitle && (
            <p className="truncate text-xs text-gray-500 italic dark:text-gray-400">{book.subtitle}</p>
          )}

          {authorDisplay && (
            <p className="truncate text-xs text-gray-600 dark:text-gray-400">{authorDisplay}</p>
          )}

          <div className="mt-auto flex flex-wrap items-center gap-2 text-xs text-gray-400">
            {book.publishedYear && <span>{book.publishedYear}</span>}
            {book.isbn && <span>ISBN {book.isbn}</span>}
            {showPlacedStatus && (
              <>
                {isPlaced ? (
                  <span className="text-green-600">● Placed</span>
                ) : (
                  <span className="text-gray-400">○ Unplaced</span>
                )}
              </>
            )}
          </div>
        </div>

        {/* Edit button */}
        <button
          onClick={() => setEditing(true)}
          title={t.books.editBook}
          className="absolute right-8 bottom-2 rounded p-1 text-gray-300 opacity-0 transition-opacity group-hover:opacity-100 hover:bg-gray-100 hover:text-gray-700 dark:hover:bg-gray-700 dark:hover:text-gray-200"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
          </svg>
        </button>

        {/* Delete button */}
        <button
          onClick={() => setConfirmDelete(true)}
          title={t.books.removeBook}
          className="absolute right-2 bottom-2 rounded p-1 text-gray-300 opacity-0 transition-opacity group-hover:opacity-100 hover:bg-red-50 hover:text-red-600 dark:hover:bg-red-900/30 dark:hover:text-red-400"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm4 0a1 1 0 012 0v6a1 1 0 11-2 0V8z" clipRule="evenodd" />
          </svg>
        </button>
      </article>

      {editing && (
        <EditBookModal userBook={userBook} onClose={() => setEditing(false)} />
      )}

      {confirmDelete && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
          onClick={() => setConfirmDelete(false)}
        >
          <div
            className="w-full max-w-sm rounded-lg bg-white p-6 shadow-xl dark:bg-gray-800"
            onClick={(e) => e.stopPropagation()}
          >
            <p className="text-sm text-gray-800 dark:text-gray-200">{t.books.confirmRemoveBook}</p>
            <p className="mt-1 truncate text-sm font-semibold text-gray-900 dark:text-gray-100">{book.title}</p>
            <div className="mt-5 flex justify-end gap-3">
              <button
                onClick={() => setConfirmDelete(false)}
                className="rounded px-4 py-2 text-sm text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700"
              >
                {t.bookshelves.cancelAdd}
              </button>
              <button
                onClick={handleDelete}
                disabled={deleting}
                className="rounded bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700 disabled:opacity-50"
              >
                {t.books.removeBook}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
