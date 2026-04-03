import { requireAdmin } from "@/lib/auth-utils";
import { getAllConnections } from "@/features/admin/devices/service";
import { Card } from "@/components/ui/Card";
import { getDict } from "@/lib/locale";

export default async function AdminConnectionsPage() {
  await requireAdmin();

  const [result, t] = await Promise.all([getAllConnections(), getDict()]);
  const connections = result.success ? result.data : [];

  return (
    <div className="flex flex-col gap-8">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">{t.admin.devicesTitle}</h1>
        <p className="text-gray-600 dark:text-gray-400">
          {t.admin.devicesSubtitle} — {connections.length}{" "}
          {connections.length !== 1 ? t.admin.registeredClientsPlural : t.admin.registeredClients}
        </p>
      </div>

      {connections.length === 0 ? (
        <Card className="border-2 border-dashed border-gray-300 dark:border-gray-600">
          <div className="flex flex-col items-center gap-4 px-6 py-16 text-center">
            <svg className="w-16 h-16 text-gray-300 dark:text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <p className="font-medium text-gray-700 dark:text-gray-300">{t.admin.noConnections}</p>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                {t.admin.noConnectionsHint}
              </p>
            </div>
          </div>
        </Card>
      ) : (
        <Card className="border-2 border-gray-200 dark:border-gray-700 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead className="bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-700/50 border-b-2 border-gray-200 dark:border-gray-700">
                <tr>
                  <th className="px-6 py-4 text-left">
                    <span className="text-xs font-semibold uppercase tracking-wider text-gray-600 dark:text-gray-400 flex items-center gap-2">
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3v-6" />
                      </svg>
                      {t.admin.colId}
                    </span>
                  </th>
                  <th className="px-6 py-4 text-left">
                    <span className="text-xs font-semibold uppercase tracking-wider text-gray-600 dark:text-gray-400 flex items-center gap-2">
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 14h8M8 10h8M6 6h12a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V8a2 2 0 012-2z" />
                      </svg>
                      {t.admin.colName}
                    </span>
                  </th>
                  <th className="px-6 py-4 text-left">
                    <span className="text-xs font-semibold uppercase tracking-wider text-gray-600 dark:text-gray-400 flex items-center gap-2">
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12a9 9 0 11-18 0 9 9 0 0118 0m-5.657-5.657l-.707-.707M5.75 12a.75.75 0 11-1.5 0 .75.75 0 011.5 0z" />
                      </svg>
                      {t.admin.colIp}
                    </span>
                  </th>
                  <th className="px-6 py-4 text-left">
                    <span className="text-xs font-semibold uppercase tracking-wider text-gray-600 dark:text-gray-400 flex items-center gap-2">
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                      </svg>
                      {t.admin.colPort}
                    </span>
                  </th>
                  <th className="px-6 py-4 text-left">
                    <span className="text-xs font-semibold uppercase tracking-wider text-gray-600 dark:text-gray-400 flex items-center gap-2">
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                      </svg>
                      {t.admin.pendingTasks}
                    </span>
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 bg-white dark:divide-gray-700 dark:bg-gray-900/50">
                {connections.map((conn) => (
                  <tr key={conn.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                    <td className="whitespace-nowrap px-6 py-4 text-sm font-mono text-gray-600 dark:text-gray-400 font-medium">{conn.id}</td>
                    <td className="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900 dark:text-gray-100">{conn.name}</td>
                    <td className="whitespace-nowrap px-6 py-4 font-mono text-sm text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800/30 px-3 py-1 rounded">{conn.ip}</td>
                    <td className="whitespace-nowrap px-6 py-4 text-sm font-medium text-indigo-600 dark:text-indigo-400 font-mono">{conn.port}</td>
                    <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-500 dark:text-gray-400">—</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}
    </div>
  );
}
