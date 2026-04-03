import { redirect } from "next/navigation";
import { getOptionalSession } from "@/lib/auth-utils";

/**
 * Root page: redirect authenticated users to the dashboard,
 * otherwise to the login page.
 */
export default async function RootPage() {
  const session = await getOptionalSession();
  if (session?.user) {
    redirect("/dashboard");
  }
  redirect("/login");
}
