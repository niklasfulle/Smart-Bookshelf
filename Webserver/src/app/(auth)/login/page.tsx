"use client";

import { useState, useTransition } from "react";
import Link from "next/link";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { loginUser } from "@/features/auth/actions";
import { useAppContext } from "@/contexts/AppContext";

export default function LoginPage() {
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();
  const { t } = useAppContext();

  const handleSubmit = (e: React.SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    const formData = new FormData(e.currentTarget);

    startTransition(async () => {
      const result = await loginUser(formData);
      if (!result.success) {
        setError(result.error.message);
      }
      // On success, the server action redirects to /dashboard.
    });
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50 p-4 dark:bg-gray-900">
      <div className="w-full max-w-sm">
        {/* Logo */}
        <div className="mb-8 flex flex-col items-center gap-2">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-600">
            <svg className="h-7 w-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25"
              />
            </svg>
          </div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Smart Bookshelf</h1>
          <p className="text-sm text-gray-500 dark:text-gray-400">{t.login.subtitle}</p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="flex flex-col gap-4 rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800"
        >
          {error && (
            <div className="rounded-md bg-red-50 px-4 py-3 text-sm text-red-700 border border-red-100 dark:bg-red-900/30 dark:text-red-400 dark:border-red-800">
              {error}
            </div>
          )}

          <Input
            label={t.login.email}
            name="email"
            type="email"
            autoComplete="email"
            required
          />

          <Input
            label={t.login.password}
            name="password"
            type="password"
            autoComplete="current-password"
            required
          />

          <Button type="submit" isLoading={isPending} className="mt-2">
            {t.login.signIn}
          </Button>
        </form>

        <p className="mt-4 text-center text-sm text-gray-500 dark:text-gray-400">
          {t.login.noAccount}{" "}
          <Link href="/register" className="font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400">
            {t.login.createOne}
          </Link>
        </p>
      </div>
    </div>
  );
}

