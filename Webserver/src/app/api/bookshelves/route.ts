import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { createBookshelf } from "@/features/bookshelves/service";
import { createBookshelfSchema } from "@/features/bookshelves/schemas";

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

  const parsed = createBookshelfSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json(
      { error: "Validation failed", issues: parsed.error.flatten().fieldErrors },
      { status: 422 },
    );
  }

  const result = await createBookshelf(session.user.id, parsed.data);
  if (!result.success) {
    return NextResponse.json({ error: result.error.message }, { status: 400 });
  }

  return NextResponse.json({ id: result.data.id }, { status: 201 });
}
