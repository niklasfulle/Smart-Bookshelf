"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  type ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import { translations, type Locale, type Dict } from "@/lib/translations";

interface AppContextValue {
  locale: Locale;
  setLocale: (l: Locale) => void;
  t: Dict;
  theme: "light" | "dark";
  toggleTheme: () => void;
}

const AppContext = createContext<AppContextValue | null>(null);

export function useAppContext() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useAppContext must be used inside AppProvider");
  return ctx;
}

interface AppProviderProps {
  children: ReactNode;
  initialLocale: Locale;
}

export function AppProvider({ children, initialLocale }: AppProviderProps) {
  const router = useRouter();
  const [locale, setLocaleState] = useState<Locale>(initialLocale);
  const [theme, setTheme] = useState<"light" | "dark">("light");

  // Read persisted theme on mount (the inline script already applied the class,
  // this just syncs the React state so the toggle button reflects the correct icon).
  useEffect(() => {
    const stored = localStorage.getItem("theme");
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const initial = (stored ?? (prefersDark ? "dark" : "light")) as "light" | "dark";
    setTheme(initial);
  }, []);

  const toggleTheme = useCallback(() => {
    setTheme((prev) => {
      const next = prev === "light" ? "dark" : "light";
      localStorage.setItem("theme", next);
      document.documentElement.classList.toggle("dark", next === "dark");
      return next;
    });
  }, []);

  const setLocale = useCallback(
    (l: Locale) => {
      setLocaleState(l);
      document.cookie = `locale=${l}; path=/; max-age=${60 * 60 * 24 * 365}; SameSite=Lax`;
      router.refresh();
    },
    [router],
  );

  return (
    <AppContext.Provider
      value={{ locale, setLocale, t: translations[locale] as Dict, theme, toggleTheme }}
    >
      {children}
    </AppContext.Provider>
  );
}
