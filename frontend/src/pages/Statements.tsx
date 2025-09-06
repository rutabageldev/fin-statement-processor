export default function Statements() {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Statements
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          View and manage your uploaded financial statements
        </p>
      </div>

      <div className="card">
        <div className="p-6">
          <div className="text-center py-12 text-gray-500 dark:text-gray-400">
            <DocumentTextIcon className="w-16 h-16 mx-auto mb-4 text-gray-300" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              No statements uploaded yet
            </h3>
            <p>Upload your first statement to see it listed here</p>
            <button className="btn-primary mt-4">
              Upload Statement
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

// Import the icon
import { DocumentTextIcon } from '@heroicons/react/24/outline'
