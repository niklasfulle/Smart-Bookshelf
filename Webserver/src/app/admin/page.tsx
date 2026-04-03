import Link from "next/link";
import { requireAdmin } from "@/lib/auth-utils";
import { getTasks } from "@/features/tasks/service";
import { getAllConnections } from "@/features/admin/devices/service";
import { prisma } from "@/lib/prisma";
import { Card, CardContent } from "@/components/ui/Card";
import { getDict } from "@/lib/locale";

export default async function AdminDashboardPage() {
  await requireAdmin();

  const [tasksResult, connectionsResult, userCount, t] = await Promise.all([
    getTasks({ pageSize: 1 }),
    getAllConnections(),
    prisma.user.count(),
    getDict(),
  ]);

  const totalTasks = tasksResult.success ? tasksResult.data.total : 0;
  const totalConnections = connectionsResult.success ? connectionsResult.data.length : 0;

  const stats = [
    { label: t.admin.users, value: userCount, href: "/admin/users" },
    { label: t.admin.connections, value: totalConnections, href: "/admin/devices" },
    { label: t.admin.tasksInQueue, value: totalTasks, href: "/admin/tasks" },
  ];

  return (
    <div className="flex flex-col gap-8">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100">{t.admin.title}</h1>
        <p className="text-base text-gray-600 dark:text-gray-400">{t.admin.subtitle}</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
        {stats.map(({ label, value, href }) => (
          <Link key={href} href={href} className="group">
            <Card className="h-full border-2 border-amber-200 dark:border-amber-900/50 hover:border-amber-400 hover:shadow-lg transition-all dark:hover:border-amber-700">
              <CardContent className="space-y-3">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">{label}</p>
                    <p className="text-4xl font-bold text-amber-600 dark:text-amber-400 mt-2">{value}</p>
                  </div>
                  <div className="text-amber-600/30 dark:text-amber-400/30 group-hover:text-amber-600/50 dark:group-hover:text-amber-400/50 transition-colors">
                    {href === "/admin/users" && (
                      <svg className="w-12 h-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 4.354a4 4 0 110 8.048M3 20.585h18M3 20.585a6 6 0 0 1 9-5.585 6 6 0 0 1 9 5.585M3 20.585A6.001 6.001 0 0 0 12 23a6.001 6.001 0 0 0 9-2.415" />
                      </svg>
                    )}
                    {href === "/admin/devices" && (
                      <svg className="w-12 h-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12a9 9 0 11-18 0 9 9 0 0118 0m-5.657-5.657l-.707-.707M5.75 12a.75.75 0 11-1.5 0 .75.75 0 011.5 0z" />
                      </svg>
                    )}
                    {href === "/admin/tasks" && (
                      <svg className="w-12 h-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    )}
                  </div>
                </div>
                <div className="pt-2 border-t border-gray-200 dark:border-gray-700">
                  <p className="text-xs text-amber-600 dark:text-amber-400 font-semibold group-hover:translate-x-1 transition-transform">View →</p>
                </div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>

      {/* Info Card */}
      <Card className="border-2 border-indigo-200/50 dark:border-indigo-900/50 bg-indigo-50/30 dark:bg-indigo-950/20">
        <CardContent className="space-y-3">
          <div className="flex gap-3">
            <svg className="w-6 h-6 text-indigo-600 dark:text-indigo-400 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div className="flex-1">
              <h3 className="font-semibold text-gray-900 dark:text-gray-100">{t.admin.hardwareStatus}</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                {t.admin.hardwareDesc}{" "}
                <Link href="/admin/devices" className="text-indigo-600 hover:text-indigo-700 dark:text-indigo-400 dark:hover:text-indigo-300 font-semibold">
                  {t.admin.hardwareLink}
                </Link>{" "}
                {t.admin.hardwareEnd}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

