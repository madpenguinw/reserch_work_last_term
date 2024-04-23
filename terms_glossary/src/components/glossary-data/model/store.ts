import { create } from 'zustand'

import GLOSSARY_RAW_DATA from '@/data/index.json'

export type DataType = typeof GLOSSARY_RAW_DATA

type GlossaryDataStore = {
  data: DataType
  changeData: (e: DataType) => void
}

export const useGlossaryData = create<GlossaryDataStore>(set => ({
  data: { ...GLOSSARY_RAW_DATA },
  changeData: e => set(() => ({ data: e }))
}))
