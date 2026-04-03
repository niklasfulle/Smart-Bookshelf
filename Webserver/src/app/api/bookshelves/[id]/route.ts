import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { updateBookshelf, deleteBookshelf } from "@/features/bookshelves/service";
import { updateBookshelfSchema } from "@/features/bookshelves/schemas";

interface RouteParams {
  params: Promise<{ id: string }>;
}

export async function PUT(req: NextRequest, { params }: RouteParams): Promise<NextResponse> {
  const session = await auth();
  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { id } = await params;

  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON" }, { status: 400 });
  }

  const parsed = updateBookshelfSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json(
      { error: "Validation failed", issues: parsed.error.flatten().fieldErrors },
      { status: 422 },
    );
  }

  const result = await updateBookshelf(session.user.id, id, parsed.data);
  if (!result.success) {
    const status = result.error.type === "NOT_FOUND" ? 404 : 400;
    return NextResponse.json({ error: result.error.message }, { status });
  }

  return NextResponse.json({ id: result.data.id });
}

export async function DELETE(_req: NextRequest, { params }: RouteParams): Promise<NextResponse> {
  const session = await auth();
  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { id } = await params;
  const result = await deleteBookshelf(session.user.id, id);
  if (!result.success) {
    const status = result.error.type === "NOT_FOUND" ? 404 : 400;
    return NextResponse.json({ error: result.error.message }, { status });
  }

  return new NextResponse(null, { status: 204 });
}
