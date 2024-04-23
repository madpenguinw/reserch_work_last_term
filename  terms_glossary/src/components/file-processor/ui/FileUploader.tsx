/* eslint-disable react-hooks/exhaustive-deps */
import { PaperClipIcon } from '@heroicons/react/24/solid'
import { ChangeEvent, FC, useEffect, useId, useState } from 'react'
import { useRef } from 'react'
import { v4 } from 'uuid'

import { parseJsonSafely } from '@/utils'

import { UploadedFileType } from '../model/types'

type Props = {
  className?: string
  disabled?: boolean
  accept?: ('image' | 'pdf' | 'doc' | 'xml')[]
  onUpload?: (data: UploadedFileType) => void
  onReadStart?: (data: UploadedFileType) => void
  onReadProgress?: (data: UploadedFileType) => void
  onReadEnd?: (data: UploadedFileType) => void
  onRead?: (data: UploadedFileType) => void
}

const FileUploader: FC<Props> = ({
  disabled,
  onUpload,
  onReadEnd,
  onRead,
  onReadStart,
  onReadProgress
}) => {
  const realInput = useRef<HTMLInputElement | null>(null)
  const htmlId = useId()
  const fileData = useRef<UploadedFileType | null>(null)
  const reader = useRef(new FileReader())

  const [loading, setLoading] = useState(false)

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    handleFile(event.target?.files?.[event.target?.files?.length - 1])
  }

  const handleClick = () => {
    if (realInput.current) {
      realInput.current.click()
    }
  }

  const handleFile = (file: File | undefined) => {
    if (loading || !file) {
      return
    }
    setLoading(true)

    const fileId = v4()
    const data = {
      id: fileId,
      file,
      data: null,
      loading: true,
      progress: 0
    }

    console.log(file)

    // reader.current.readAsDataURL(file)
    // eslint-disable-next-line unicorn/prefer-blob-reading-methods
    reader.current.readAsText(file)

    onUpload?.(data)
    fileData.current = data
  }

  const onFileReadStart = (event: ProgressEvent<FileReader>) => {
    if (!fileData.current) {
      return
    }

    const data = {
      ...fileData.current,
      data: (event.target?.result as string) || null
    }

    onReadStart?.(data)
    onRead?.(data)
    fileData.current = data
  }

  const onFileReadProgress = (event: ProgressEvent<FileReader>) => {
    if (!fileData.current) {
      return
    }

    const progress = Math.round((event.loaded / event.total) * 100)

    const data = {
      ...fileData.current,
      url: (event.target?.result as string) || null,
      progress
    }

    onReadProgress?.(data)
    onRead?.(data)
    fileData.current = data
  }

  const onFileRead = (event: ProgressEvent<FileReader>) => {
    if (!fileData.current) {
      return
    }

    const data = {
      ...fileData.current,
      data: (event.target?.result as string) || null,
      loading: false
    }

    console.log(data, parseJsonSafely(data.data))
    onRead?.(data)
    onReadEnd?.(data)

    fileData.current = null
    setLoading(false)

    if (realInput.current) {
      realInput.current.value = ''
    }
  }

  useEffect(() => {
    if (!reader.current) {
      return
    }

    reader.current.addEventListener('load', onFileRead)
    reader.current.addEventListener('loadstart', onFileReadStart)
    reader.current.addEventListener('progress', onFileReadProgress)

    return () => {
      if (!reader.current) {
        return
      }

      reader.current.removeEventListener('load', onFileRead)
      reader.current.removeEventListener('loadstart', onFileReadStart)
      reader.current.removeEventListener('progress', onFileReadProgress)
    }
  }, [])

  return (
    <div>
      <label htmlFor={htmlId} className="flex" onClick={handleClick}>
        <input
          ref={realInput}
          disabled={disabled || loading}
          id={htmlId}
          multiple={false}
          accept=".txt, .json"
          type="file"
          className="peer hidden"
          style={{ display: 'none' }}
          onChange={handleChange}
        />
        <button className="flex items-center gap-x-4 transition peer-disabled:opacity-70">
          <PaperClipIcon className="h-16 w-16" />
          <span className="text-slate-600 text-12">Загрузить файл</span>
        </button>
      </label>
    </div>
  )
}

export default FileUploader
