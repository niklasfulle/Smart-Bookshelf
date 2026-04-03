import { prisma } from "@/lib/prisma";
import { createConnectionSchema, updateConnectionSchema } from "./schemas";
import type { CreateConnectionInput, UpdateConnectionInput } from "./schemas";
import { type Result, ok, err, notFound, internalError } from "@/lib/errors";
import type { Connection } from "@prisma/client";

export async function createConnection(input: CreateConnectionInput): Promise<Result<Connection>> {
  const parsed = createConnectionSchema.safeParse(input);
  if (!parsed.success) {
    return err({
      type: "VALIDATION_ERROR",
      message: "Invalid connection data",
      issues: parsed.error.flatten().fieldErrors as Record<string, string[]>,
    });
  }

  try {
    const connection = await prisma.connection.create({ data: parsed.data });
    return ok(connection);
  } catch {
    return err(internalError("Failed to create connection"));
  }
}

export async function getAllConnections(): Promise<Result<Connection[]>> {
  try {
    const connections = await prisma.connection.findMany({
      orderBy: { id: "asc" },
    });
    return ok(connections);
  } catch {
    return err(internalError("Failed to fetch connections"));
  }
}

export async function getConnectionById(id: number): Promise<Result<Connection>> {
  const connection = await prisma.connection.findUnique({ where: { id } });
  if (!connection) return err(notFound("Connection not found"));
  return ok(connection);
}

export async function updateConnection(
  id: number,
  input: UpdateConnectionInput,
): Promise<Result<Connection>> {
  const parsed = updateConnectionSchema.safeParse(input);
  if (!parsed.success) {
    return err({
      type: "VALIDATION_ERROR",
      message: "Invalid connection data",
      issues: parsed.error.flatten().fieldErrors as Record<string, string[]>,
    });
  }

  const existing = await prisma.connection.findUnique({ where: { id } });
  if (!existing) return err(notFound("Connection not found"));

  try {
    const updated = await prisma.connection.update({ where: { id }, data: parsed.data });
    return ok(updated);
  } catch {
    return err(internalError("Failed to update connection"));
  }
}

export async function deleteConnection(id: number): Promise<Result<void>> {
  const existing = await prisma.connection.findUnique({ where: { id } });
  if (!existing) return err(notFound("Connection not found"));

  await prisma.connection.delete({ where: { id } });
  return ok(undefined);
}
