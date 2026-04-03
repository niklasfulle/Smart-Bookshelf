"use client";

import { useState, useTransition } from "react";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import type { BookMetadata } from "@/features/books/import-service";

interface BookImportFormProps {
  onMetadataFound?: (metadata: BookMetadata) => void;
  onManualEntry?: () => void;
}

type LookupMode = "isbn" | "barcode";

/**
 * Form for importing a book by ISBN or barcode.
 * On submit, calls the /api/books/lookup server route to fetch metadata,
 * then surfaces it to the parent via onMetadataFound.
 */
export function BookImportForm({ onMetadataFound, onManualEntry }: BookImportFormProps) {
  const [mode, setMode] = useState<LookupMode>("isbn");
  const [value, setValue] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  const handleSubmit = (e: React.SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);

    const trimmed = value.trim();
    if (!trimmed) {
      setError("Please enter a value");
      return;
    }

    startTransition(async () => {
      try {
        const res = await fetch(`/api/books/lookup?type=${mode}&value=${encodeURIComponent(trimmed)}`);
        const json = await res.json() as { metadata?: BookMetadata; error?: string };

        if (!res.ok || json.error) {
          setError(json.error ?? "No book found. Try entering details manually.");
          return;
        }

        if (json.metadata) {
          onMetadataFound?.(json.metadata);
        }
      } catch {
        setError("Network error. Please try again.");
      }
    });
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      {/* Mode toggle */}
      <div className="flex rounded-md border border-gray-200 bg-gray-50 p-1" role="group">
        {(["isbn", "barcode"] as const).map((m) => (
          <button
            key={m}
            type="button"
            onClick={() => {
              setMode(m);
              setValue("");
              setError(null);
            }}
            className={[
              "flex-1 rounded py-1.5 text-sm font-medium transition-colors",
              mode === m
                ? "bg-white text-gray-900 shadow-sm"
                : "text-gray-500 hover:text-gray-700",
            ].join(" ")}
          >
            {m === "isbn" ? "ISBN" : "Barcode"}
          </button>
        ))}
      </div>

      <Input
        label={mode === "isbn" ? "ISBN (10 or 13 digits)" : "Barcode (EAN-13 / UPC)"}
        type="text"
        inputMode="numeric"
        pattern="[\d\-X]+"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder={mode === "isbn" ? "e.g. 978-3-16-148410-0" : "e.g. 9783161484100"}
        error={error ?? undefined}
        required
      />

      <div className="flex gap-3">
        <Button type="submit" isLoading={isPending} className="flex-1">
          Look up
        </Button>
        {onManualEntry && (
          <Button type="button" variant="secondary" onClick={onManualEntry}>
            Enter manually
          </Button>
        )}
      </div>
    </form>
  );
}
