"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { useAppContext } from "@/contexts/AppContext";
import type { ShelfWithPlacements } from "@/features/bookshelves/service";

interface CollectionBook {
  id: string;
  book: {
    id: string;
    title: string;
    authors: string[];
    coverUrl: string | null;
  };
}

interface AddBookModalProps {
  bookshelfId: string;
  shelves: ShelfWithPlacements[];
}

export function AddBookButton({ bookshelfId, shelves }: Readonly<AddBookModalProps>) {
  const { t } = useAppContext();
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="inline-flex items-center rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors dark:border-gray-600 dark:bg-gray-800 dark:text-gray-200 dark:hover:bg-gray-700"
      >
        {t.bookshelves.addBook}
      </button>
      {open && (
        <AddBookModal
          bookshelfId={bookshelfId}
          shelves={shelves}
          onClose={() => setOpen(false)}
        />
      )}
    </>
  );
}

interface ModalProps extends AddBookModalProps {
  onClose: () => void;
}

function AddBookModal({ bookshelfId, shelves, onClose }: Readonly<ModalProps>) {
  const { t } = useAppContext();
  const router = useRouter();

  const [books, setBooks] = useState<CollectionBook[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [selectedBook, setSelectedBook] = useState<CollectionBook | null>(null);
  const [selectedShelfId, setSelectedShelfId] = useState(shelves[0]?.id ?? "");
  const [placing, setPlacing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchBooks = useCallback(async (q: string) => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ onlyUnplaced: "true" });
      if (q) params.append("q", q);
      const url = `/api/books/collection?${params.toString()}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error("Failed to load collection");
      const data = (await res.json()) as { items: CollectionBook[] };
      setBooks(data.items);
    } catch {
      setError("Failed to load collection");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void fetchBooks("");
  }, [fetchBooks]);

  useEffect(() => {
    const timer = setTimeout(() => void fetchBooks(search), 300);
    return () => clearTimeout(timer);
  }, [search, fetchBooks]);

  async function handlePlace() {
    if (!selectedBook || !selectedShelfId) return;
    setPlacing(true);
    setError(null);
    try {
      const shelf = shelves.find((s) => s.id === selectedShelfId);
      const position = shelf ? shelf.placements.length : 0;
      const res = await fetch("/api/placements", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          userBookId: selectedBook.id,
          bookshelfId,
          shelfId: selectedShelfId,
          position,
        }),
      });
      if (!res.ok) {
        const data = (await res.json()) as { error?: string };
        throw new Error(data.error ?? "Failed to place book");
      }
      
      const responseData = await res.json() as { placement?: any };
      
      // Dispatch event so BookshelfDnd can update immediately
      if (responseData.placement) {
        window.dispatchEvent(new CustomEvent('placement-added', { 
          detail: { placement: responseData.placement } 
        }));
      }
      
      setPlacing(false);
      onClose();
      router.refresh();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to place book");
    } finally {
      setPlacing(false);
    }
  }

  const sortedShelves = [...shelves].sort((a, b) => a.order - b.order);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
      <div className="w-full max-w-md rounded-xl bg-white shadow-2xl dark:bg-gray-900 flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="flex items-center border-b border-gray-200 px-6 py-4 dark:border-gray-700">
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xl leading-none -ml-6"
            aria-label="Close"
          >
            ✕
          </button>
          <h2 className="ml-4 text-lg font-semibold text-gray-900 dark:text-gray-100">
            {t.bookshelves.addBookTitle}
          </h2>
        </div>

        {/* Shelf selector */}
        {sortedShelves.length > 0 && (
          <div className="px-6 pt-4">
            <label className="mb-1 block text-xs font-medium text-gray-600 dark:text-gray-400">
              {t.bookshelves.selectShelf}
            </label>
            <select
              value={selectedShelfId}
              onChange={(e) => setSelectedShelfId(e.target.value)}
              className="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100"
            >
              {sortedShelves.map((shelf) => (
                <option key={shelf.id} value={shelf.id}>
                  {shelf.name ?? `${t.bookshelves.shelfLabel} ${shelf.order}`}
                </option>
              ))}
            </select>
          </div>
        )}

        {/* Search */}
        <div className="px-6 pt-3">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder={t.bookshelves.searchBooks}
            className="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 placeholder-gray-400 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 dark:placeholder-gray-500"
          />
        </div>

        {/* Book list */}
        <div className="flex-1 overflow-y-auto px-6 py-3">
          {loading && <p className="py-4 text-center text-sm text-gray-400">…</p>}
          {!loading && books.length === 0 && (
            <p className="py-4 text-center text-sm text-gray-500 dark:text-gray-400">
              {t.bookshelves.noCollectionBooks}
            </p>
          )}
          {!loading && books.length > 0 && (
            <ul className="flex flex-col gap-1">
              {books.map((ub) => (
                <li key={ub.id}>
                  <button
                    onClick={() => setSelectedBook(ub)}
                    className={`w-full rounded-lg px-3 py-2 text-left transition-colors ${
                      selectedBook?.id === ub.id
                        ? "bg-indigo-100 text-indigo-900 dark:bg-indigo-900/40 dark:text-indigo-100"
                        : "hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-800 dark:text-gray-100"
                    }`}
                  >
                    <p className="text-sm font-medium leading-tight">{ub.book.title}</p>
                    {ub.book.authors.length > 0 && (
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        {ub.book.authors.join(", ")}
                      </p>
                    )}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Error */}
        {error && (
          <p className="px-6 pb-2 text-xs text-red-500">{error}</p>
        )}

        {/* Footer */}
        <div className="flex justify-end gap-2 border-t border-gray-200 px-6 py-4 dark:border-gray-700">
          <button
            onClick={onClose}
            className="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-800"
          >
            {t.bookshelves.cancelAdd}
          </button>
          <button
            onClick={() => void handlePlace()}
            disabled={!selectedBook || !selectedShelfId || placing}
            className="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {placing ? "…" : t.bookshelves.placeBook}
          </button>
        </div>
      </div>
    </div>
  );
}
