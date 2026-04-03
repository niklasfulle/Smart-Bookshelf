import type { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  className?: string;
}

export function Card({ children, className = "" }: CardProps) {
  return (
    <div className={["rounded-lg border border-gray-200 bg-white shadow-sm dark:border-gray-700 dark:bg-gray-800", className].join(" ")}>
      {children}
    </div>
  );
}

export function CardHeader({ children, className = "" }: CardProps) {
  return (
    <div className={["border-b border-gray-200 px-6 py-4 dark:border-gray-700", className].join(" ")}>
      {children}
    </div>
  );
}

export function CardContent({ children, className = "" }: CardProps) {
  return <div className={["px-6 py-4", className].join(" ")}>{children}</div>;
}

export function CardFooter({ children, className = "" }: CardProps) {
  return (
    <div className={["border-t border-gray-200 px-6 py-3 dark:border-gray-700", className].join(" ")}>
      {children}
    </div>
  );
}
