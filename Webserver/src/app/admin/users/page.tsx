import { requireAdmin } from "@/lib/auth-utils";
import { prisma } from "@/lib/prisma";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { getDict } from "@/lib/locale";
import type { Role } from "@prisma/client";

const roleBadgeVariant: Record<Role, "indigo" | "gray"> = {
  ADMIN: "indigo",
  USER: "gray",
};

export default async function AdminUsersPage() {
  await requireAdmin();

  const [users, t] = await Promise.all([
    prisma.user.findMany({
      select: { id: true, name: true, email: true, role: true, createdAt: true },
      orderBy: { createdAt: "desc" },
    }),
    getDict(),
  ]);

  return (
    <div className="flex flex-col gap-8">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">{t.admin.usersTitle}</h1>
        <p className="text-gray-600 dark:text-gray-400">
          {users.length} {t.admin.registeredUsers}
        </p>
      </div>

      {/* Users Table */}
      <Card className="border-2 border-gray-200 dark:border-gray-700 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className="bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-700/50 border-b-2 border-gray-200 dark:border-gray-700">
              <tr>
                <th className="px-6 py-4 text-left">
                  <span className="text-xs font-semibold uppercase tracking-wider text-gray-600 dark:text-gray-400 flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {t.admin.colName}
                  </span>
                </th>
                <th className="px-6 py-4 text-left">
                  <span className="text-xs font-semibold uppercase tracking-wider text-gray-600 dark:text-gray-400 flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                    {t.admin.colEmail}
                  </span>
                </th>
                <th className="px-6 py-4 text-left">
                  <span className="text-xs font-semibold uppercase tracking-wider text-gray-600 dark:text-gray-400 flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                    </svg>
                    {t.admin.colRole}
                  </span>
                </th>
                <th className="px-6 py-4 text-left">
                  <span className="text-xs font-semibold uppercase tracking-wider text-gray-600 dark:text-gray-400 flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {t.admin.colJoined}
                  </span>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 bg-white dark:divide-gray-700 dark:bg-gray-900/50">
              {users.length === 0 ? (
                <tr>
                  <td colSpan={4} className="px-6 py-12 text-center">
                    <div className="flex flex-col items-center gap-2">
                      <svg className="w-12 h-12 text-gray-300 dark:text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 4.354a4 4 0 110 8.048M3 20.585h18M3 20.585a6 6 0 0 1 9-5.585 6 6 0 0 1 9 5.585M3 20.585A6.001 6.001 0 0 0 12 23a6.001 6.001 0 0 0 9-2.415" />
                      </svg>
                      <p className="text-gray-500 dark:text-gray-400">No users found</p>
                    </div>
                  </td>
                </tr>
              ) : (
                users.map((user) => (
                  <tr key={user.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="inline-flex items-center gap-2">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-400 to-indigo-600 flex items-center justify-center text-white text-xs font-semibold">
                          {(user.name ?? "U")?.[0]?.toUpperCase()}
                        </div>
                        <span className="font-medium text-gray-900 dark:text-gray-100">{user.name ?? "—"}</span>
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                      {user.email}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <Badge variant={roleBadgeVariant[user.role]}>{user.role}</Badge>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                      {new Date(user.createdAt).toLocaleDateString("de-DE", { year: "numeric", month: "2-digit", day: "2-digit" })}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
