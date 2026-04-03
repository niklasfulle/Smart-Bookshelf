import { z } from "zod";

export const createConnectionSchema = z.object({
  name: z.string().min(1, "Name is required").max(200),
  ip: z.string().ip({ message: "Invalid IP address" }),
  port: z.number().int().min(1, "Port must be at least 1").max(65535, "Port must be at most 65535"),
});

export const updateConnectionSchema = createConnectionSchema.partial();

export type CreateConnectionInput = z.infer<typeof createConnectionSchema>;
export type UpdateConnectionInput = z.infer<typeof updateConnectionSchema>;
