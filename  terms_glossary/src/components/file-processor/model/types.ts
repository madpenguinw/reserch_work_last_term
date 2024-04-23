export type UploadedFileType = {
  id: string
  file: File | null
  data: string | null
  loading: boolean
  progress: number
}
