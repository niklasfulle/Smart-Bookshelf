import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { moveBookPlacement } from "@/features/bookshelves/service";
import { prisma } from "@/lib/prisma";
import { z } from "zod";

const moveSchema = z.object({
  shelfId: z.string().cuid(),
  position: z.number().int().min(0),
});

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

  const parsed = moveSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json(
      { error: "Validation failed", issues: parsed.error.flatten().fieldErrors },
      { status: 422 },
    );
  }

  const result = await moveBookPlacement(
    session.user.id,
    id,
    parsed.data.shelfId,
    parsed.data.position,
  );

  if (!result.success) {
    const status = result.error.type === "NOT_FOUND" ? 404 : 500;
    return NextResponse.json({ error: result.error.message }, { status });
  }

  // Fetch the complete placement with userBook and book data
  const placement = await prisma.bookPlacement.findUnique({
    where: { id: result.data.id },
    include: { userBook: { include: { book: true } } },
  });

  return NextResponse.json({ placement });
}
