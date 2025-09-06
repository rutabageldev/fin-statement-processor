import { useState } from 'react'
import { DocumentArrowUpIcon } from '@heroicons/react/24/outline'

export default function Upload() {
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    // Handle file drop logic here
    const files = Array.from(e.dataTransfer.files)
    console.log('Files dropped:', files)
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Upload Statement
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Upload your PDF statement and CSV transaction files
        </p>
      </div>

      <div className="max-w-2xl mx-auto">
        <div className="card p-8">
          <div
            className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
              dragActive
                ? 'border-primary-400 bg-primary-50 dark:bg-primary-900/20'
                : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <DocumentArrowUpIcon className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              Drop your files here
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              PDF statements and CSV transaction files supported
            </p>
            <button className="btn-primary">
              Choose Files
            </button>
          </div>

          <div className="mt-6">
            <h4 className="font-medium text-gray-900 dark:text-white mb-3">
              Supported Formats:
            </h4>
            <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
              <li>• PDF statement files (up to 10MB)</li>
              <li>• CSV transaction files (up to 10MB)</li>
              <li>• Currently supports Citi Credit Card statements</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
