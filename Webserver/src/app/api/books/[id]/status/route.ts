import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { updateUserBook } from "@/features/books/service";
import { z } from "zod";
import type { CollectionStatus } from "@prisma/client";

const updateStatusSchema = z.object({
  status: z.enum(["OWNED", "READING", "READ", "WISHLIST", "LENT_OUT"] as const).optional(),
  notes: z.string().optional(),
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

  const parsed = updateStatusSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json(
      { error: "Validation failed", issues: parsed.error.flatten().fieldErrors },
      { status: 422 },
    );
  }

  const result = await updateUserBook(session.user.id, id, {
    status: parsed.data.status as CollectionStatus | undefined,
    notes: parsed.data.notes,
  });

  if (!result.success) {
    const status = result.error.type === "NOT_FOUND" ? 404 : 500;
    return NextResponse.json({ error: result.error.message }, { status });
  }

  return NextResponse.json(result.data);
}
