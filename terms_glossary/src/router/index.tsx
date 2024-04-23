import {
  createBrowserRouter,
  createRoutesFromElements,
  Route
} from 'react-router-dom'

import { LayoutDefault } from '@/layout/LayoutDefault'
import { ErrorPage } from '@/pages/ErrorPage'
import { HomePage } from '@/pages/HomePage'
import { MindMapView } from '@/pages/MindMapView'
import { Root } from '@/Root'

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<Root />} errorElement={<ErrorPage />}>
      <Route element={<LayoutDefault />}>
        <Route index element={<HomePage />} />
        <Route path="/mindmap" element={<MindMapView />} />
      </Route>
    </Route>
  )
)

export default router
