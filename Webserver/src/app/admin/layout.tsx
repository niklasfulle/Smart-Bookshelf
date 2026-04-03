"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState, useEffect } from "react";

const adminLinks = [
  { 
    href: "/admin/users", 
    label: "Users", 
    description: "Manage user accounts and roles",
    icon: "users"
  },
  { 
    href: "/admin/devices", 
    label: "Connections", 
    description: "Manage ESP32 client connections",
    icon: "devices"
  },
  { 
    href: "/admin/tasks", 
    label: "Tasks", 
    description: "Monitor and manage the task queue",
    icon: "tasks"
  },
];

const getIcon = (icon: string) => {
  switch (icon) {
    case "users":
      return (
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 8.048M3 20.585h18M3 20.585a6 6 0 0 1 9-5.585 6 6 0 0 1 9 5.585M3 20.585A6.001 6.001 0 0 0 12 23a6.001 6.001 0 0 0 9-2.415" />
        </svg>
      );
    case "devices":
      return (
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 14h8M8 10h8M6 6h12a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V8a2 2 0 012-2z" />
        </svg>
      );
    case "tasks":
      return (
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
        </svg>
      );
    default:
      return null;
  }
};

function AdminSidebar() {
  const pathname = usePathname();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <aside className="hidden w-64 flex-shrink-0 lg:block">
        <div className="sticky top-20 space-y-2">
          <div className="h-32 rounded-lg bg-gradient-to-br from-indigo-600 to-indigo-700 animate-pulse" />
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="h-16 rounded-lg bg-gray-200 dark:bg-gray-700 animate-pulse" />
          ))}
        </div>
      </aside>
    );
  }
  
  return (
    <aside className="hidden w-64 flex-shrink-0 lg:block px-2 py-8">
      <div className="sticky top-24 space-y-3">
        {/* Back Link */}
        <Link
          href="/dashboard"
          className="flex items-center gap-2 rounded-lg border-2 border-gray-200 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 hover:border-indigo-400 hover:bg-indigo-50 transition-all dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:border-indigo-500 dark:hover:bg-indigo-950/30"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Zurück
        </Link>

        {/* Header */}
        <div className="rounded-lg bg-gradient-to-br from-indigo-600 to-indigo-700 p-4 text-white shadow-lg">
          <div className="flex items-center gap-2 mb-1">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 6.5C9.514 6.5 7.5 8.514 7.5 11c0 2.486 2.014 4.5 4.5 4.5s4.5-2.014 4.5-4.5c0-2.486-2.014-4.5-4.5-4.5zm0 8c-1.933 0-3.5-1.567-3.5-3.5S10.067 8 12 8s3.5 1.567 3.5 3.5-1.567 3.5-3.5 3.5zM12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z" />
            </svg>
            <p className="text-sm font-bold tracking-wide">ADMIN</p>
          </div>
          <p className="text-xs text-indigo-100">Control Panel</p>
        </div>

        {/* Navigation */}
        <nav className="space-y-2">
          {adminLinks.map(({ href, label, description, icon }) => {
            const isActive = pathname === href || pathname?.startsWith(href);
            return (
              <Link
                key={href}
                href={href}
                className={[
                  "group flex items-start gap-3 rounded-lg border-2 px-4 py-3 transition-all",
                  isActive
                    ? "border-indigo-400 bg-indigo-50 shadow-md dark:border-indigo-500 dark:bg-indigo-950/30"
                    : "border-gray-200 bg-white hover:border-indigo-400 hover:bg-indigo-50 hover:shadow-md dark:border-gray-700 dark:bg-gray-800 dark:hover:border-indigo-500 dark:hover:bg-indigo-950/30"
                ].join(" ")}
              >
                <div className={[
                  "mt-0.5 transition-colors",
                  isActive
                    ? "text-indigo-600 dark:text-indigo-400"
                    : "text-gray-400 group-hover:text-indigo-600 dark:text-gray-500 dark:group-hover:text-indigo-400"
                ].join(" ")}>
                  {getIcon(icon)}
                </div>
                <div className="min-w-0 flex-1">
                  <p className={[
                    "text-sm font-semibold transition-colors",
                    isActive
                      ? "text-indigo-600 dark:text-indigo-400"
                      : "text-gray-900 group-hover:text-indigo-600 dark:text-gray-100 dark:group-hover:text-indigo-400"
                  ].join(" ")}>
                    {label}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 line-clamp-1">
                    {description}
                  </p>
                </div>
              </Link>
            );
          })}
        </nav>
      </div>
    </aside>
  );
}

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(false);
  }, []);

  if (isLoading) {
    return null;
  }

  return (
    <div className="flex gap-8 min-h-screen bg-white dark:bg-gray-900">
      <AdminSidebar />
      <main className="min-w-0 flex-1 px-6 sm:px-8 py-8 overflow-x-hidden">
        <div className="mx-auto max-w-7xl">
          {children}
        </div>
      </main>
    </div>
  );
}
