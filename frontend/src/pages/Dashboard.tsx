export default function Dashboard() {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Dashboard
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Overview of your financial data and recent activity
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Placeholder cards */}
        <div className="card p-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Recent Spending
          </h2>
          <div className="text-center py-12 text-gray-500 dark:text-gray-400">
            No data available yet. Upload your first statement to get started.
          </div>
        </div>

        <div className="card p-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Category Breakdown
          </h2>
          <div className="text-center py-12 text-gray-500 dark:text-gray-400">
            Charts will appear here once you have transaction data.
          </div>
        </div>
      </div>
    </div>
  )
}
