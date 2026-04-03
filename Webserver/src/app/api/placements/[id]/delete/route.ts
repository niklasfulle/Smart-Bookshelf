import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";

export async function DELETE(
  req: NextRequest,
  { params }: { params: Promise<{ id: string }> },
): Promise<NextResponse> {
  const session = await auth();
  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { id } = await params;

  const placement = await prisma.bookPlacement.findUnique({
    where: { id },
    include: {
      shelf: {
        include: { bookshelf: true },
      },
    },
  });

  if (!placement) {
    return NextResponse.json({ error: "Placement not found" }, { status: 404 });
  }

  // Verify ownership
  if (placement.shelf.bookshelf.userId !== session.user.id) {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  // Delete the placement
  await prisma.bookPlacement.delete({
    where: { id },
  });

  return NextResponse.json({ success: true });
}
