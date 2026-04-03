import { z } from "zod";

export const createBookshelfSchema = z.object({
  name: z.string().min(1, "Name is required").max(200),
  description: z.string().max(1000).optional(),
  location: z.string().max(200).optional(),
});

export const updateBookshelfSchema = createBookshelfSchema.partial();

export const createShelfSchema = z.object({
  bookshelfId: z.string().cuid("Invalid bookshelf ID"),
  order: z.number().int().min(1, "Order must be at least 1"),
  name: z.string().max(100).optional(),
  widthCm: z.number().positive("Width in cm is required").max(100, "Width cannot exceed 100cm"),
  heightCm: z.number().positive().optional(),
  depthCm: z.number().positive().optional(),
});

export const updateShelfSchema = createShelfSchema.omit({ bookshelfId: true }).partial();

export const placeBookSchema = z.object({
  userBookId: z.string().cuid("Invalid user book ID"),
  bookshelfId: z.string().cuid("Invalid bookshelf ID"),
  shelfId: z.string().cuid("Invalid shelf ID"),
  position: z.number().int().min(0, "Position must be non-negative"),
  widthSpan: z.number().positive().optional(),
});

export type CreateBookshelfInput = z.infer<typeof createBookshelfSchema>;
export type UpdateBookshelfInput = z.infer<typeof updateBookshelfSchema>;
export type CreateShelfInput = z.infer<typeof createShelfSchema>;
export type PlaceBookInput = z.infer<typeof placeBookSchema>;
