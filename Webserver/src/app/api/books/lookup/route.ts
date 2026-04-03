import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import {
  fetchBookMetadataByIsbn,
  fetchBookMetadataByBarcode,
} from "@/features/books/import-service";
import { isbnSchema, barcodeSchema } from "@/features/books/schemas";

/**
 * GET /api/books/lookup?type=isbn&value=...
 * GET /api/books/lookup?type=barcode&value=...
 *
 * Looks up book metadata from an external provider.
 * Requires authentication.
 */
export async function GET(req: NextRequest): Promise<NextResponse> {
  const session = await auth();
  if (!session?.user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { searchParams } = req.nextUrl;
  const type = searchParams.get("type");
  const value = searchParams.get("value");

  if (!type || !value) {
    return NextResponse.json({ error: "Missing type or value parameter" }, { status: 400 });
  }

  if (type === "isbn") {
    const parsed = isbnSchema.safeParse(value);
    if (!parsed.success) {
      return NextResponse.json({ error: "Invalid ISBN format" }, { status: 400 });
    }

    const metadata = await fetchBookMetadataByIsbn(parsed.data);
    if (!metadata) {
      return NextResponse.json({ error: "No book found for this ISBN" }, { status: 404 });
    }

    return NextResponse.json({ metadata });
  }

  if (type === "barcode") {
    const parsed = barcodeSchema.safeParse(value);
    if (!parsed.success) {
      return NextResponse.json({ error: "Invalid barcode format" }, { status: 400 });
    }

    const metadata = await fetchBookMetadataByBarcode(parsed.data);
    if (!metadata) {
      return NextResponse.json({ error: "No book found for this barcode" }, { status: 404 });
    }

    return NextResponse.json({ metadata });
  }

  return NextResponse.json({ error: "Type must be 'isbn' or 'barcode'" }, { status: 400 });
}
