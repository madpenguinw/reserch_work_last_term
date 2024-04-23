import { FC } from 'react'
import { Outlet } from 'react-router-dom'

import { AppHeader } from '@/components/header'

const LayoutDefault: FC = () => {
  return (
    <>
      <AppHeader />
      <main className="pt-30">
        <Outlet />
      </main>
    </>
  )
}

export { LayoutDefault }
