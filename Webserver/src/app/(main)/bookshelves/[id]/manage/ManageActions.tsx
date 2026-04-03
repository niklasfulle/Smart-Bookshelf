"use client";

import { useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { useAppContext } from "@/contexts/AppContext";

// ---------------------------------------------------------------------------
// Edit bookshelf details form
// ---------------------------------------------------------------------------
interface EditFormProps {
  bookshelfId: string;
  initialName: string;
  initialDescription?: string | null;
  initialLocation?: string | null;
}

export function EditBookshelfInline({
  bookshelfId,
  initialName,
  initialDescription,
  initialLocation,
}: EditFormProps) {
  const router = useRouter();
  const { t } = useAppContext();
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [globalError, setGlobalError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  const handleSubmit = (e: React.SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErrors({});
    setGlobalError(null);

    const data = new FormData(e.currentTarget);
    const input = {
      name: String(data.get("name") ?? ""),
      description: String(data.get("description") ?? "") || undefined,
      location: String(data.get("location") ?? "") || undefined,
    };

    startTransition(async () => {
      const res = await fetch(`/api/bookshelves/${bookshelfId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(input),
      });

      const json = await res.json() as { id?: string; error?: string; issues?: Record<string, string[]> };

      if (!res.ok) {
        if (json.issues) {
          const fieldErrors: Record<string, string> = {};
          for (const [field, msgs] of Object.entries(json.issues)) {
            fieldErrors[field] = msgs[0];
          }
          setErrors(fieldErrors);
        } else {
          setGlobalError(json.error ?? t.bookshelves.failedUpdate);
        }
        return;
      }

      router.refresh();
    });
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      {globalError && (
        <div className="rounded-md bg-red-50 px-4 py-3 text-sm text-red-700 border border-red-100 dark:bg-red-900/30 dark:text-red-400 dark:border-red-800">
          {globalError}
        </div>
      )}
      <Input
        label={t.newBookshelf.name}
        name="name"
        required
        defaultValue={initialName}
        placeholder={t.newBookshelf.namePlaceholder}
        error={errors.name}
      />
      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium text-gray-700 dark:text-gray-200">
          {t.newBookshelf.description}
        </label>
        <textarea
          name="description"
          rows={2}
          defaultValue={initialDescription ?? ""}
          placeholder={t.newBookshelf.descPlaceholder}
          className="block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 dark:placeholder:text-gray-500"
        />
      </div>
      <Input
        label={t.newBookshelf.location}
        name="location"
        defaultValue={initialLocation ?? ""}
        placeholder={t.newBookshelf.locPlaceholder}
        error={errors.location}
      />
      <div className="flex justify-end">
        <Button type="submit" isLoading={isPending} size="sm">
          {t.bookshelves.saveChanges}
        </Button>
      </div>
    </form>
  );
}

// ---------------------------------------------------------------------------
// Add shelf level form
// ---------------------------------------------------------------------------
interface AddShelfFormProps {
  bookshelfId: string;
  nextOrder: number;
}

export function AddShelfForm({ bookshelfId, nextOrder }: AddShelfFormProps) {
  const router = useRouter();
  const { t } = useAppContext();
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();
  const [widthCm, setWidthCm] = useState<number>(80); // Default 80cm

  // Calculate zones from width (1 zone = 3.5cm)
  const BOOK_WIDTH_CM = 3.5;
  const calcDropZones = Math.max(1, Math.floor(widthCm / BOOK_WIDTH_CM));

  const handleSubmit = (e: React.SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    const data = new FormData(e.currentTarget);

    const input = {
      bookshelfId,
      order: nextOrder,
      name: String(data.get("name") ?? "") || undefined,
      widthCm: widthCm || 80,
    };

    startTransition(async () => {
      const res = await fetch("/api/shelves", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(input),
      });

      if (!res.ok) {
        const json = await res.json() as { error?: string };
        setError(json.error ?? "Failed to add shelf");
        return;
      }

      (e.target as HTMLFormElement).reset();
      router.refresh();
    });
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 rounded-lg border border-gray-300 p-4 dark:border-gray-600">
      {error && <p className="text-sm text-red-600 dark:text-red-400">{error}</p>}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="flex flex-col gap-1">
          <label className="text-xs font-medium text-gray-700 dark:text-gray-200">
            {t.bookshelves.shelfNameLabel}
          </label>
          <input
            name="name"
            placeholder={t.bookshelves.shelfNamePlaceholder}
            className="rounded-md border border-gray-300 px-3 py-2 text-sm dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 dark:placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-300"
          />
        </div>
        <div className="flex flex-col gap-1">
          <label className="text-xs font-medium text-gray-700 dark:text-gray-200">
            {t.bookshelves.widthLabel}
          </label>
          <div className="flex items-center gap-2">
            <input
              type="number"
              min="1"
              max="100"
              placeholder={t.bookshelves.widthPlaceholder}
              value={widthCm}
              onChange={(e) => setWidthCm(Math.min(100, Math.max(1, Number(e.target.value) || 80)))}
              className="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 dark:placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-300"
            />
            <span className="text-xs text-gray-600 dark:text-gray-400">cm</span>
          </div>
          <p className="text-xs text-gray-600 dark:text-gray-400">
            {calcDropZones} {calcDropZones === 1 ? 'zone' : 'zones'}
          </p>
        </div>
      </div>
      <Button type="submit" size="sm" isLoading={isPending}>
        {t.bookshelves.addShelfLevel} #{nextOrder}
      </Button>
    </form>
  );
}

// ---------------------------------------------------------------------------
// Delete shelf button
// ---------------------------------------------------------------------------
interface DeleteShelfButtonProps {
  shelfId: string;
}

export function DeleteShelfButton({ shelfId }: DeleteShelfButtonProps) {
  const router = useRouter();
  const { t } = useAppContext();
  const [isPending, startTransition] = useTransition();
  const [showConfirm, setShowConfirm] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function handleConfirm() {
    setError(null);
    startTransition(async () => {
      const res = await fetch(`/api/shelves/${shelfId}`, { method: "DELETE" });
      
      if (!res.ok) {
        const json = await res.json() as { error?: string };
        setError(json.error ?? "Failed to delete shelf");
        return;
      }

      setShowConfirm(false);
      router.refresh();
    });
  }

  return (
    <>
      <button
        onClick={() => setShowConfirm(true)}
        disabled={isPending}
        aria-label={t.bookshelves.remove}
        className="flex h-6 w-6 items-center justify-center rounded text-gray-400 transition-colors hover:text-red-600 hover:bg-red-50 disabled:opacity-40 dark:hover:bg-red-900/30 dark:hover:text-red-400"
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

      {showConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
          <div className="w-full max-w-sm rounded-xl bg-white p-6 shadow-2xl dark:bg-gray-900">
            {error && (
              <p className="mb-4 text-sm text-red-600 dark:text-red-400">{error}</p>
            )}
            <p className="text-sm text-gray-700 dark:text-gray-200">
              {t.bookshelves.confirmDeleteShelf}
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
                onClick={handleConfirm}
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
