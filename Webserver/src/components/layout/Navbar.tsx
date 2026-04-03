"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { signOut } from "next-auth/react";
import { useState } from "react";
import type { Role } from "@prisma/client";
import { useAppContext } from "@/contexts/AppContext";

interface NavbarProps {
  userName?: string | null;
  userRole: Role;
}

export function Navbar({ userName, userRole }: NavbarProps) {
  const pathname = usePathname();
  const { t, locale, setLocale, theme, toggleTheme } = useAppContext();
  const [menuOpen, setMenuOpen] = useState(false);

  const navLinks = [
    { href: "/dashboard", label: t.nav.dashboard },
    { href: "/bookshelves", label: t.nav.bookshelves },
    { href: "/books", label: t.nav.myBooks },
  ];

  return (
    <header className="sticky top-0 z-40 border-b border-gray-200 bg-white shadow-sm dark:border-gray-700 dark:bg-gray-900">
      <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4 sm:px-6">
        {/* Logo */}
        <Link
          href="/dashboard"
          className="flex items-center gap-2 font-semibold text-gray-900 dark:text-gray-100"
        >
          <svg
            className="h-6 w-6 text-indigo-600"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25"
            />
          </svg>
          Smart Bookshelf
        </Link>

        {/* Nav links */}
        <nav className="hidden md:flex items-center gap-1">
          {navLinks.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className={[
                "rounded-md px-3 py-2 text-sm font-medium transition-colors",
                pathname === href || pathname.startsWith(href + "/")
                  ? "bg-indigo-50 text-indigo-700 dark:bg-indigo-900/40 dark:text-indigo-200"
                  : "text-gray-600 hover:bg-gray-100 hover:text-gray-900 dark:text-gray-200 dark:hover:bg-gray-800 dark:hover:text-white",
              ].join(" ")}
            >
              {label}
            </Link>
          ))}
          {userRole === "ADMIN" && (
            <Link
              href="/admin"
              className={[
                "rounded-md px-3 py-2 text-sm font-medium transition-colors",
                pathname.startsWith("/admin")
                  ? "bg-indigo-50 text-indigo-700 dark:bg-indigo-900/40 dark:text-indigo-200"
                  : "text-gray-600 hover:bg-gray-100 hover:text-gray-900 dark:text-gray-200 dark:hover:bg-gray-800 dark:hover:text-white",
              ].join(" ")}
            >
              {t.nav.admin}
            </Link>
          )}
        </nav>

        {/* Right-side controls */}
        <div className="flex items-center gap-2">
          {/* Language toggle */}
          <button
            onClick={() => setLocale(locale === "en" ? "de" : "en")}
            className="rounded-md px-2 py-1.5 text-xs font-semibold text-gray-500 hover:bg-gray-100 hover:text-gray-900 transition-colors dark:text-gray-200 dark:hover:bg-gray-800 dark:hover:text-white"
            aria-label="Toggle language"
            title={locale === "en" ? "Auf Deutsch wechseln" : "Switch to English"}
          >
            {locale === "en" ? "DE" : "EN"}
          </button>

          {/* Theme toggle */}
          <button
            onClick={toggleTheme}
            className="rounded-md p-1.5 text-gray-500 hover:bg-gray-100 hover:text-gray-900 transition-colors dark:text-gray-200 dark:hover:bg-gray-800 dark:hover:text-white"
            aria-label="Toggle theme"
            title={theme === "light" ? "Switch to dark mode" : "Switch to light mode"}
          >
            {theme === "light" ? (
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
                />
              </svg>
            ) : (
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707M17.657 17.657l-.707-.707M6.343 6.343l-.707-.707M12 7a5 5 0 100 10A5 5 0 0012 7z"
                />
              </svg>
            )}
          </button>

          {/* User menu */}
          <div className="relative">
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="flex items-center gap-1 rounded-md px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 transition-colors dark:text-gray-200 dark:hover:bg-gray-800 dark:hover:text-white"
            >
              <span className="hidden sm:block">{userName ?? "User"}</span>
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </button>

            {/* Dropdown menu */}
            {menuOpen && (
              <div
                className="absolute right-0 top-full z-50 mt-1 w-48 rounded-lg border border-gray-200 bg-white shadow-lg dark:border-gray-700 dark:bg-gray-800"
                onClick={() => setMenuOpen(false)}
              >
                <div className="py-1">
                  {userRole === "ADMIN" && (
                    <Link
                      href="/admin"
                      className="flex items-center gap-3 px-4 py-2 text-sm text-gray-900 hover:bg-gray-100 dark:text-gray-100 dark:hover:bg-gray-700"
                    >
                      <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                      </svg>
                      {t.nav.admin}
                    </Link>
                  )}
                  <Link
                    href="/settings/password"
                    className="flex items-center gap-3 px-4 py-2 text-sm text-gray-900 hover:bg-gray-100 dark:text-gray-100 dark:hover:bg-gray-700"
                  >
                    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                    {t.nav.changePassword || "Change password"}
                  </Link>
                  <button
                    onClick={() => signOut({ callbackUrl: "/login" })}
                    className="flex w-full items-center gap-3 px-4 py-2 text-sm text-gray-900 hover:bg-gray-100 dark:text-gray-100 dark:hover:bg-gray-700"
                  >
                    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    {t.nav.signOut}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}

