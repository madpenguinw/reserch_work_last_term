import { FC } from 'react'
import { Outlet } from 'react-router-dom'

export const Root: FC = () => {
  return (
    <>
      <Outlet />
    </>
  )
}
