"use client";

import { useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";

interface AddShelfFormProps {
  bookshelfId: string;
  nextOrder: number;
}

export function AddShelfForm({ bookshelfId, nextOrder }: AddShelfFormProps) {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  const handleSubmit = (e: React.SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    const data = new FormData(e.currentTarget);

    const input = {
      bookshelfId,
      order: nextOrder,
      name: String(data.get("name") ?? "") || undefined,
      widthCm: data.get("widthCm") ? Number(data.get("widthCm")) : undefined,
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
    <form onSubmit={handleSubmit} className="flex flex-wrap items-end gap-3">
      {error && (
        <p className="w-full text-sm text-red-600 dark:text-red-400">{error}</p>
      )}
      <div className="flex flex-col gap-1">
        <label className="text-xs font-medium text-gray-600 dark:text-gray-400">Name (optional)</label>
        <input
          name="name"
          placeholder="e.g. Top shelf"
          className="rounded-md border border-gray-300 px-3 py-2 text-sm dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 dark:placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-300"
        />
      </div>
      <div className="flex flex-col gap-1">
        <label className="text-xs font-medium text-gray-600 dark:text-gray-400">Width (cm, optional)</label>
        <input
          name="widthCm"
          type="number"
          min="1"
          placeholder="e.g. 80"
          className="w-28 rounded-md border border-gray-300 px-3 py-2 text-sm dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 dark:placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-300"
        />
      </div>
      <Button type="submit" size="sm" isLoading={isPending}>
        Add shelf level
      </Button>
    </form>
  );
}

interface DeleteShelfButtonProps {
  shelfId: string;
}

export function DeleteShelfButton({ shelfId }: DeleteShelfButtonProps) {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();

  function handleDelete() {
    startTransition(async () => {
      await fetch(`/api/shelves/${shelfId}`, { method: "DELETE" });
      router.refresh();
    });
  }

  return (
    <Button variant="danger" size="sm" isLoading={isPending} onClick={handleDelete}>
      Remove
    </Button>
  );
}
