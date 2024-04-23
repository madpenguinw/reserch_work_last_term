import { FC, useState } from 'react'

import { FileDownloader, FileUploader } from '@/components/file-processor'
import { UploadedFileType } from '@/components/file-processor/model/types'
import { Glossary } from '@/components/glossary'
import { type DataType, useGlossaryData } from '@/components/glossary-data'
import { parseJsonSafely } from '@/utils'

const checkDataValidity = (e: DataType) => {
  if (
    'nodes' in e &&
    'edges' in e &&
    Array.isArray(e.nodes) &&
    Array.isArray(e.edges)
  ) {
    return true
  }

  return false
}

export const HomePage: FC = () => {
  const { data, changeData } = useGlossaryData()
  const [uploadError, setUploadError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleUploadData = (_e: UploadedFileType) => {
    setUploadError('')
    setLoading(true)
  }

  const handleUploadEndData = (e: UploadedFileType) => {
    const _data = parseJsonSafely(e.data)
    setLoading(false)
    if (!_data) {
      return setUploadError('Не удалось загрузить данные')
    }
    if (!checkDataValidity(_data as DataType)) {
      return setUploadError('Неверный формат данных')
    }

    changeData(_data as DataType)
  }
  return (
    <div className="p-20 lg:p-16">
      <div className="mb-30 flex justify-between gap-y-10">
        <div className="mb-10 flex cursor-pointer flex-col font-medium text-12">
          <span>Соколов Михаил</span>
          <span>P4208</span>
        </div>
        <div className="flex flex-col gap-x-10">
          <FileUploader
            onUpload={handleUploadData}
            onReadEnd={handleUploadEndData}
            disabled={loading}
          />
          <FileDownloader downloadedDataObject={data} disabled={loading} />
        </div>
      </div>
      {uploadError && (
        <div className="flex items-center">
          <div className="rounded-5 bg-red-400 px-10 py-8 text-white text-12">
            {uploadError}
          </div>
        </div>
      )}

      {!loading && <Glossary />}
    </div>
  )
}
