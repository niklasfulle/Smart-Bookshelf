import { forwardRef, type InputHTMLAttributes } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(function Input(
  { label, error, hint, id, className = "", ...props },
  ref,
) {
  const inputId = id ?? label?.toLowerCase().replaceAll(/\s+/g, "-");

  return (
    <div className="flex flex-col gap-1">
      {label && (
        <label htmlFor={inputId} className="text-sm font-medium text-gray-700 dark:text-gray-200">
          {label}
          {props.required && <span className="ml-1 text-red-500">*</span>}
        </label>
      )}
      <input
        ref={ref}
        id={inputId}
        className={[
          "block w-full rounded-md border px-3 py-2 text-sm shadow-sm",
          "bg-white text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-0",
          "dark:bg-gray-700 dark:text-gray-100 dark:placeholder:text-gray-500",
          error
            ? "border-red-400 focus:border-red-400 focus:ring-red-300 dark:border-red-500"
            : "border-gray-300 focus:border-indigo-400 focus:ring-indigo-300 dark:border-gray-600 dark:focus:border-indigo-500",
          "disabled:cursor-not-allowed disabled:bg-gray-50 disabled:text-gray-500 dark:disabled:bg-gray-800",
          className,
        ].join(" ")}
        {...props}
      />
      {hint && !error && <p className="text-xs text-gray-500">{hint}</p>}
      {error && <p className="text-xs text-red-600">{error}</p>}
    </div>
  );
});
