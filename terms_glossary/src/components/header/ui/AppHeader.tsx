import clsx from 'clsx'
import { FC } from 'react'
import { NavLink } from 'react-router-dom'

const AppHeader: FC = () => {
  return (
    <header className="fixed left-0 right-0 top-0 z-[50] flex h-30 items-center justify-center bg-white px-20 py-10 shadow-md lg:px-16">
      <div className="flex items-center gap-x-10">
        <NavLink
          to="/"
          className={({ isActive }) =>
            clsx('text-12', { 'text-blue-500': isActive })
          }
        >
          Глоссарий
        </NavLink>
        <NavLink
          to="/mindmap"
          className={({ isActive }) =>
            clsx('text-12', { 'text-blue-500': isActive })
          }
        >
          Граф
        </NavLink>
      </div>
    </header>
  )
}

export default AppHeader
