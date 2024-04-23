import { FC } from 'react'

import { useGlossaryData } from '@/components/glossary-data'

const Glossary: FC = () => {
  const { data } = useGlossaryData()

  return (
    <>
      <div className="grid grid-cols-5 gap-10 xl:grid-cols-4 lg:grid-cols-3 md:grid-cols-2 sm:grid-cols-1">
        {data.nodes.map(node => (
          <div
            key={node.id}
            className="bg-gray-100 px-15 py-20 transition hover:bg-gray-200"
          >
            <p className="mb-10 font-medium text-18">{node.label}</p>
            <p className="text-14">{node.description}</p>
          </div>
        ))}
      </div>
    </>
  )
}

export default Glossary
