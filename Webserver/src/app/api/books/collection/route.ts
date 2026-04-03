import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { getUserBooks, addBookToCollection } from "@/features/books/service";
import type { CreateBookInput } from "@/features/books/schemas";

export async function GET(req: NextRequest): Promise<NextResponse> {
  const session = await auth();
  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { searchParams } = new URL(req.url);
  const search = searchParams.get("q") ?? undefined;
  const pageSize = Math.min(Number(searchParams.get("pageSize") ?? "100"), 200);
  const onlyUnplaced = searchParams.get("onlyUnplaced") === "true";

  const result = await getUserBooks(session.user.id, { search, pageSize, onlyUnplaced });
  if (!result.success) {
    return NextResponse.json({ error: result.error.message }, { status: 500 });
  }

  return NextResponse.json(result.data);
}

export async function POST(req: NextRequest): Promise<NextResponse> {
  const session = await auth();
  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON" }, { status: 400 });
  }

  const result = await addBookToCollection(session.user.id, body as CreateBookInput);
  if (!result.success) {
    let status = 500;
    if (result.error.type === "CONFLICT") status = 409;
    else if (result.error.type === "VALIDATION_ERROR") status = 422;
    return NextResponse.json({ error: result.error.message }, { status });
  }

  return NextResponse.json({ id: result.data.id }, { status: 201 });
}
