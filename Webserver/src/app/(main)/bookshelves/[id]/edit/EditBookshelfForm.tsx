"use client";

import { useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardHeader } from "@/components/ui/Card";
import { useAppContext } from "@/contexts/AppContext";

interface EditBookshelfFormProps {
  bookshelfId: string;
  initialName: string;
  initialDescription?: string | null;
  initialLocation?: string | null;
}

export function EditBookshelfForm({
  bookshelfId,
  initialName,
  initialDescription,
  initialLocation,
}: EditBookshelfFormProps) {
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
          setGlobalError(json.error ?? "Failed to update bookshelf");
        }
        return;
      }

      router.push(`/bookshelves/${bookshelfId}`);
      router.refresh();
    });
  }

  return (
    <div className="mx-auto max-w-lg">
      <div className="mb-6">
        <Link
          href={`/bookshelves/${bookshelfId}`}
          className="text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
        >
          ← {t.bookshelves.title}
        </Link>
        <h1 className="mt-2 text-2xl font-bold text-gray-900 dark:text-gray-100">
          {t.newBookshelf.name} bearbeiten
        </h1>
      </div>

      <Card>
        <CardHeader>
          <p className="text-sm text-gray-500 dark:text-gray-400">{t.newBookshelf.hint}</p>
        </CardHeader>
        <CardContent>
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
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                {t.newBookshelf.description}
              </label>
              <textarea
                name="description"
                rows={3}
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

            <div className="flex justify-end gap-3 pt-2">
              <Link
                href={`/bookshelves/${bookshelfId}`}
                className="inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors dark:border-gray-600 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600"
              >
                {t.newBookshelf.cancel}
              </Link>
              <Button type="submit" isLoading={isPending}>
                Speichern
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
