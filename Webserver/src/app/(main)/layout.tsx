import { requireAuth } from "@/lib/auth-utils";
import { Navbar } from "@/components/layout/Navbar";

export default async function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await requireAuth();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar userName={session.user.name} userRole={session.user.role} />
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6">{children}</main>
    </div>
  );
}
