import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { getTasks, deleteTask } from "@/features/tasks/service";

/**
 * GET /api/tasks/next?clientId=<n>
 *
 * Returns the oldest pending task for a given client (FIFO, as the Raspberry Pi
 * server expects). Returns 204 if no tasks are pending.
 *
 * Note: The Raspberry Pi server (ESP32_Server/server.py) reads directly from
 * PostgreSQL via psycopg2 and deletes tasks after processing. This endpoint
 * is provided for debugging and future REST-based integrations.
 */
export async function GET(req: NextRequest): Promise<NextResponse> {
  const session = await auth();
  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const clientIdParam = req.nextUrl.searchParams.get("clientId");
  const clientId = clientIdParam ? Number(clientIdParam) : undefined;

  const result = await getTasks({ clientId, pageSize: 1 });
  if (!result.success) {
    return NextResponse.json({ error: result.error.message }, { status: 500 });
  }

  if (result.data.items.length === 0) {
    return new NextResponse(null, { status: 204 });
  }

  return NextResponse.json({ task: result.data.items[0] });
}

/**
 * DELETE /api/tasks/next?id=<n>
 *
 * Deletes a task by integer ID (mirrors what the Raspberry Pi server does after processing).
 */
export async function DELETE(req: NextRequest): Promise<NextResponse> {
  const session = await auth();
  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const idParam = req.nextUrl.searchParams.get("id");
  const id = idParam ? Number(idParam) : Number.NaN;

  if (Number.isNaN(id) || id <= 0) {
    return NextResponse.json({ error: "Invalid or missing id parameter" }, { status: 400 });
  }

  const result = await deleteTask(id);
  if (!result.success) {
    return NextResponse.json(
      { error: result.error.message },
      { status: result.error.type === "NOT_FOUND" ? 404 : 500 },
    );
  }

  return new NextResponse(null, { status: 204 });
}
