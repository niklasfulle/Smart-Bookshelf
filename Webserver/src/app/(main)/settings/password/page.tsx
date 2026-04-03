"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Card, CardContent } from "@/components/ui/Card";
import { useAppContext } from "@/contexts/AppContext";

export default function ChangePasswordPage() {
  const router = useRouter();
  const { t } = useAppContext();
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setSuccess(false);

    if (newPassword !== confirmPassword) {
      setError(t.settings.passwordMismatch);
      return;
    }

    if (newPassword.length < 8) {
      setError(t.settings.passwordTooShort);
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("/api/auth/change-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ currentPassword, newPassword }),
      });

      if (!res.ok) {
        const data = await res.json();
        setError(data.error || t.settings.failedChangePassword);
        return;
      }

      setSuccess(true);
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");

      setTimeout(() => {
        router.push("/dashboard");
      }, 2000);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-md py-12">
      <Card>
        <CardContent>
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">{t.settings.changePasswordTitle}</h1>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">{t.settings.changePasswordSubtitle}</p>
          </div>

          {error && (
            <div className="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-700 dark:bg-red-900/20 dark:text-red-400">
              {error}
            </div>
          )}

          {success && (
            <div className="mb-4 rounded-lg bg-green-50 p-3 text-sm text-green-700 dark:bg-green-900/20 dark:text-green-400">
              {t.settings.passwordChanged}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <label className="block">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-200">{t.settings.currentPasswordLabel}</span>
              <input
                type="password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                required
                className="mt-1 w-full rounded-lg border border-gray-300 px-4 py-2 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100"
              />
            </label>

            <label className="block">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-200">{t.settings.newPasswordLabel}</span>
              <input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
                className="mt-1 w-full rounded-lg border border-gray-300 px-4 py-2 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100"
              />
            </label>

            <label className="block">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-200">{t.settings.confirmPasswordLabel}</span>
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                className="mt-1 w-full rounded-lg border border-gray-300 px-4 py-2 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100"
              />
            </label>

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-lg bg-indigo-600 px-4 py-2 font-medium text-white hover:bg-indigo-700 disabled:opacity-50 dark:bg-indigo-700 dark:hover:bg-indigo-600"
            >
              {loading ? t.settings.changingPassword : t.settings.changePasswordBtn}
            </button>
          </form>

          <div className="mt-6 text-center">
            <Link href="/dashboard" className="text-sm text-indigo-600 hover:text-indigo-500 dark:text-indigo-400">
              {t.settings.backToDashboard}
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
