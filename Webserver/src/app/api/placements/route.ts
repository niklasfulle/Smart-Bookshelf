import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { placeBook } from "@/features/bookshelves/service";
import { placeBookSchema } from "@/features/bookshelves/schemas";
import { prisma } from "@/lib/prisma";

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

  const parsed = placeBookSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json(
      { error: "Validation failed", issues: parsed.error.flatten().fieldErrors },
      { status: 422 },
    );
  }

  const result = await placeBook(session.user.id, parsed.data);
  if (!result.success) {
    let status = 400;
    if (result.error.type === "CONFLICT") status = 409;
    else if (result.error.type === "NOT_FOUND") status = 404;
    return NextResponse.json({ error: result.error.message }, { status });
  }

  // Fetch the complete placement with userBook and book data
  const placement = await prisma.bookPlacement.findUnique({
    where: { id: result.data.id },
    include: { userBook: { include: { book: true } } },
  });

  return NextResponse.json({ placement }, { status: 201 });
}
