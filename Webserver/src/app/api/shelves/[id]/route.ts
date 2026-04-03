import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { deleteShelf } from "@/features/bookshelves/service";

interface RouteParams {
  params: Promise<{ id: string }>;
}

export async function DELETE(_req: NextRequest, { params }: RouteParams): Promise<NextResponse> {
  const session = await auth();
  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { id } = await params;
  const result = await deleteShelf(session.user.id, id);
  if (!result.success) {
    const status = result.error.type === "NOT_FOUND" ? 404 : 400;
    return NextResponse.json({ error: result.error.message }, { status });
  }

  return new NextResponse(null, { status: 204 });
}
