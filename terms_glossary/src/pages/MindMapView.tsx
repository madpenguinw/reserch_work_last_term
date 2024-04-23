import { FC } from 'react'

import { MindMap } from '@/components/mind-map'

export const MindMapView: FC = () => {
  return (
    <>
      <MindMap className="h-[calc(100vh-30px)]" />
    </>
  )
}
