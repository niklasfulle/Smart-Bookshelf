import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { updateBookDetails, removeBookFromCollection } from "@/features/books/service";

export async function PATCH(
  req: NextRequest,
  { params }: { params: Promise<{ id: string }> },
): Promise<NextResponse> {
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

  const {
    title, subtitle, authors, coverImageUrl, spineColor, publisher, publishedYear,
  } = body as {
    title?: string;
    subtitle?: string;
    authors?: string[];
    coverImageUrl?: string | null;
    spineColor?: string | null;
    publisher?: string;
    publishedYear?: number;
  };

  const result = await updateBookDetails(session.user.id, id, {
    title, subtitle, authors, coverImageUrl, spineColor, publisher, publishedYear,
  });

  if (!result.success) {
    const status = result.error.type === "NOT_FOUND" ? 404 : 500;
    return NextResponse.json({ error: result.error.message }, { status });
  }

  return NextResponse.json(result.data);
}

export async function DELETE(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> },
): Promise<NextResponse> {
  const session = await auth();
  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { id } = await params;
  const result = await removeBookFromCollection(session.user.id, id);

  if (!result.success) {
    const status = result.error.type === "NOT_FOUND" ? 404 : 500;
    return NextResponse.json({ error: result.error.message }, { status });
  }

  return new NextResponse(null, { status: 204 });
}
