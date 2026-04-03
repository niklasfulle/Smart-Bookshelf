"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAppContext } from "@/contexts/AppContext";
import type { BookMetadata } from "@/features/books/import-service";

export function AddBookButton() {
  const { t } = useAppContext();
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-medium text-white hover:bg-indigo-700 transition-colors"
      >
        {t.books.addBook}
      </button>
      {open && <AddBookModal onClose={() => setOpen(false)} />}
    </>
  );
}

interface AddBookModalProps {
  onClose: () => void;
}

function AddBookModal({ onClose }: Readonly<AddBookModalProps>) {
  const { t } = useAppContext();
  const router = useRouter();

  const [isbn, setIsbn] = useState("");
  const [looking, setLooking] = useState(false);
  const [found, setFound] = useState<BookMetadata | null>(null);
  const [lookupError, setLookupError] = useState<string | null>(null);
  const [adding, setAdding] = useState(false);
  const [addError, setAddError] = useState<string | null>(null);

  async function handleLookup(e: React.SyntheticEvent) {
    e.preventDefault();
    if (!isbn.trim()) return;
    setLooking(true);
    setFound(null);
    setLookupError(null);
    setAddError(null);
    try {
      const res = await fetch(`/api/books/lookup?type=isbn&value=${encodeURIComponent(isbn.trim())}`);
      if (!res.ok) {
        setLookupError(t.books.isbnNotFound);
        return;
      }
      const data = (await res.json()) as { metadata: BookMetadata };
      setFound(data.metadata);
    } catch {
      setLookupError(t.books.isbnNotFound);
    } finally {
      setLooking(false);
    }
  }

  async function handleAdd() {
    if (!found) return;
    setAdding(true);
    setAddError(null);
    try {
      const res = await fetch("/api/books/collection", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...found, isbn: isbn.trim() }),
      });
      if (!res.ok) {
        const data = (await res.json()) as { error?: string };
        if (res.status === 409) {
          setAddError(t.books.alreadyInCollection);
        } else {
          setAddError(data.error ?? "Failed to add book");
        }
        return;
      }
      router.refresh();
      onClose();
    } catch {
      setAddError("Failed to add book");
    } finally {
      setAdding(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
      <div className="w-full max-w-md rounded-xl bg-white shadow-2xl dark:bg-gray-900 flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-gray-200 px-6 py-4 dark:border-gray-700">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            {t.books.addBook}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xl leading-none"
            aria-label="Close"
          >
            ✕
          </button>
        </div>

        {/* ISBN lookup */}
        <form onSubmit={(e) => void handleLookup(e)} className="flex flex-col gap-4 px-6 py-5">
          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-gray-700 dark:text-gray-200">
              {t.books.isbnLabel}
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={isbn}
                onChange={(e) => { setIsbn(e.target.value); setFound(null); setLookupError(null); }}
                placeholder={t.books.isbnPlaceholder}
                className="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm text-gray-900 placeholder-gray-400 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-300"
              />
              <button
                type="submit"
                disabled={!isbn.trim() || looking}
                className="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50 transition-colors"
              >
                {looking ? "…" : t.books.lookupBtn}
              </button>
            </div>
          </div>

          {lookupError && (
            <p className="text-sm text-red-500 dark:text-red-400">{lookupError}</p>
          )}

          {/* Found book preview */}
          {found && (
            <div className="rounded-lg border border-gray-200 bg-gray-50 p-4 dark:border-gray-700 dark:bg-gray-800">
              <p className="font-semibold text-gray-900 dark:text-gray-100">{found.title}</p>
              {found.subtitle && (
                <p className="text-sm text-gray-600 dark:text-gray-400">{found.subtitle}</p>
              )}
              {found.authors.length > 0 && (
                <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                  {found.authors.join(", ")}
                </p>
              )}
              {found.publisher && (
                <p className="mt-1 text-xs text-gray-400">{found.publisher}{found.publishedYear ? `, ${found.publishedYear}` : ""}</p>
              )}
            </div>
          )}

          {addError && (
            <p className="text-sm text-red-500 dark:text-red-400">{addError}</p>
          )}
        </form>

        {/* Footer */}
        <div className="flex justify-end gap-2 border-t border-gray-200 px-6 py-4 dark:border-gray-700">
          <button
            onClick={onClose}
            className="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-800"
          >
            {t.bookshelves.cancelAdd}
          </button>
          <button
            onClick={() => void handleAdd()}
            disabled={!found || adding}
            className="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {adding ? "…" : t.books.confirmAdd}
          </button>
        </div>
      </div>
    </div>
  );
}
