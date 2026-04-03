import { notFound } from "next/navigation";
import { requireAuth } from "@/lib/auth-utils";
import { getBookshelfById } from "@/features/bookshelves/service";
import { EditBookshelfForm } from "./EditBookshelfForm";

interface EditBookshelfPageProps {
  params: Promise<{ id: string }>;
}

export default async function EditBookshelfPage({ params }: EditBookshelfPageProps) {
  const session = await requireAuth();
  const { id } = await params;
  const result = await getBookshelfById(session.user.id, id);

  if (!result.success) notFound();

  const { name, description, location } = result.data;

  return (
    <EditBookshelfForm
      bookshelfId={id}
      initialName={name}
      initialDescription={description}
      initialLocation={location}
    />
  );
}
