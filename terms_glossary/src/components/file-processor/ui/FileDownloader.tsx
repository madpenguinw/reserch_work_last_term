import { ArrowDownTrayIcon } from '@heroicons/react/24/solid'
import { FC } from 'react'

import { saveTemplateAsFile } from '../model'

type Props = {
  className?: string
  disabled?: boolean
  downloadedDataObject?: object | any
}

const FileDownloader: FC<Props> = ({ disabled, downloadedDataObject }) => {
  const handleDownloadClick = () => {
    if (!downloadedDataObject) {
      return
    }

    const fileName = `pract-graph_${new Date()
      .toISOString()
      .replaceAll('.', '_')}.json`
    saveTemplateAsFile(fileName, downloadedDataObject)
  }

  return (
    <div>
      <button
        className="flex items-center gap-x-4 transition peer-disabled:opacity-70"
        disabled={disabled}
        onClick={handleDownloadClick}
      >
        <ArrowDownTrayIcon className="h-16 w-16" />
        <span className="text-slate-600 text-12">Скачать файл</span>
      </button>
    </div>
  )
}

export default FileDownloader
