import { prisma } from "@/lib/prisma";
import { createTaskSchema, validateTaskData, type CreateTaskInput, type TaskType } from "./schemas";
import { type Result, ok, err, notFound, internalError } from "@/lib/errors";
import type { Task } from "@prisma/client";

// ---------------------------------------------------------------------------
// Task creation (web app writes tasks for Raspberry Pi to consume)
// ---------------------------------------------------------------------------

/**
 * Creates a task row in the "tasks" table.
 * The Raspberry Pi server reads tasks ordered by createdAt ASC and deletes
 * each row after processing — no status column exists at the DB level.
 */
export async function createTask(input: CreateTaskInput): Promise<Result<Task>> {
  const parsed = createTaskSchema.safeParse(input);
  if (!parsed.success) {
    return err({
      type: "VALIDATION_ERROR",
      message: "Invalid task data",
      issues: parsed.error.flatten().fieldErrors as Record<string, string[]>,
    });
  }

  const dataValidation = validateTaskData(parsed.data.type as TaskType, parsed.data.data);
  if (!dataValidation.success) {
    return err({
      type: "VALIDATION_ERROR",
      message: `Invalid data for task type "${parsed.data.type}": ${dataValidation.error}`,
    });
  }

  try {
    const task = await prisma.task.create({
      data: {
        type: parsed.data.type,
        clientId: parsed.data.clientId,
        data: parsed.data.data ?? null,
      },
    });
    return ok(task);
  } catch {
    return err(internalError("Failed to create task"));
  }
}

// ---------------------------------------------------------------------------
// Task queries
// ---------------------------------------------------------------------------

export async function getTaskById(taskId: number): Promise<Result<Task>> {
  const task = await prisma.task.findUnique({ where: { id: taskId } });
  if (!task) return err(notFound("Task not found"));
  return ok(task);
}

export async function getTasks(options: {
  type?: string;
  clientId?: number;
  page?: number;
  pageSize?: number;
} = {}): Promise<Result<{ items: Task[]; total: number }>> {
  const { type, clientId, page = 1, pageSize = 50 } = options;

  try {
    const where = {
      ...(type ? { type } : {}),
      ...(clientId !== undefined ? { clientId } : {}),
    };

    const [items, total] = await Promise.all([
      prisma.task.findMany({
        where,
        include: { client: true },
        orderBy: { createdAt: "asc" },
        skip: (page - 1) * pageSize,
        take: pageSize,
      }),
      prisma.task.count({ where }),
    ]);

    return ok({ items, total });
  } catch {
    return err(internalError("Failed to fetch tasks"));
  }
}

/**
 * Deletes a task by ID (mirrors what the Raspberry Pi server does after processing).
 */
export async function deleteTask(taskId: number): Promise<Result<void>> {
  const task = await prisma.task.findUnique({ where: { id: taskId } });
  if (!task) return err(notFound("Task not found"));

  await prisma.task.delete({ where: { id: taskId } });
  return ok(undefined);
}

/**
 * Deletes all tasks for a given client (e.g. when removing a connection).
 */
export async function deleteTasksForClient(clientId: number): Promise<Result<number>> {
  try {
    const result = await prisma.task.deleteMany({ where: { clientId } });
    return ok(result.count);
  } catch {
    return err(internalError("Failed to delete tasks"));
  }
}


