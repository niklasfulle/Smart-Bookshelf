import { z } from "zod";

// ---------------------------------------------------------------------------
// ISBN / Barcode validation helpers
// ---------------------------------------------------------------------------

function isValidIsbn10(isbn: string): boolean {
  const digits = isbn.replaceAll(/[-\s]/g, "");
  if (digits.length !== 10) return false;
  let sum = 0;
  for (let i = 0; i < 9; i++) {
    sum += Number.parseInt(digits[i], 10) * (10 - i);
  }
  const last = digits[9].toUpperCase();
  sum += last === "X" ? 10 : Number.parseInt(last, 10);
  return sum % 11 === 0;
}

function isValidIsbn13(isbn: string): boolean {
  const digits = isbn.replaceAll(/[-\s]/g, "");
  if (digits.length !== 13) return false;
  let sum = 0;
  for (let i = 0; i < 12; i++) {
    sum += Number.parseInt(digits[i], 10) * (i % 2 === 0 ? 1 : 3);
  }
  const checkDigit = (10 - (sum % 10)) % 10;
  return checkDigit === Number.parseInt(digits[12], 10);
}

export const isbnSchema = z
  .string()
  .min(10, "ISBN must be at least 10 characters")
  .max(17, "ISBN is too long")
  .refine(
    (val) => {
      const cleaned = val.replaceAll(/[-\s]/g, "");
      return isValidIsbn10(cleaned) || isValidIsbn13(cleaned);
    },
    { message: "Invalid ISBN checksum" },
  );

export const barcodeSchema = z
  .string()
  .min(8, "Barcode must be at least 8 characters")
  .max(20, "Barcode is too long")
  .regex(/^\d+$/, "Barcode must contain only digits");

// ---------------------------------------------------------------------------
// Book creation / import schema
// ---------------------------------------------------------------------------

export const createBookSchema = z.object({
  isbn: isbnSchema.optional(),
  barcode: barcodeSchema.optional(),
  title: z.string().min(1, "Title is required").max(500),
  subtitle: z.string().max(500).optional(),
  authors: z.array(z.string().min(1)).min(1, "At least one author is required"),
  publisher: z.string().max(200).optional(),
  publishedYear: z.number().int().min(1, "Year must be positive").optional(),
  coverImageUrl: z.string().url("Invalid URL").optional(),
  spineColor: z
    .string()
    .regex(/^#[0-9a-fA-F]{6}$/, "Spine color must be a hex color code")
    .optional(),
  pageCount: z.number().int().min(1).optional(),
  language: z.string().max(10).optional(),
  widthCm: z.number().positive().optional(),
  heightCm: z.number().positive().optional(),
  thicknessCm: z.number().positive().optional(),
});

export const importByIdentifierSchema = z.union([
  z.object({ type: z.literal("isbn"), value: isbnSchema }),
  z.object({ type: z.literal("barcode"), value: barcodeSchema }),
]);

export type CreateBookInput = z.infer<typeof createBookSchema>;
export type ImportByIdentifierInput = z.infer<typeof importByIdentifierSchema>;
