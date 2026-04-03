import type { ReactNode } from "react";

interface BadgeProps {
  children: ReactNode;
  variant?: "gray" | "green" | "yellow" | "red" | "indigo" | "blue";
  size?: "sm" | "md";
}

const variantClasses: Record<NonNullable<BadgeProps["variant"]>, string> = {
  gray: "bg-gray-100 text-gray-700",
  green: "bg-green-100 text-green-700",
  yellow: "bg-yellow-100 text-yellow-700",
  red: "bg-red-100 text-red-700",
  indigo: "bg-indigo-100 text-indigo-700",
  blue: "bg-blue-100 text-blue-700",
};

const sizeClasses: Record<NonNullable<BadgeProps["size"]>, string> = {
  sm: "px-2 py-0.5 text-xs",
  md: "px-2.5 py-1 text-sm",
};

export function Badge({ children, variant = "gray", size = "sm" }: BadgeProps) {
  return (
    <span
      className={[
        "inline-flex items-center rounded-full font-medium",
        variantClasses[variant],
        sizeClasses[size],
      ].join(" ")}
    >
      {children}
    </span>
  );
}
