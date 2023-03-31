import { useState } from 'react'

function Dog() {
  const [count, setCount] = useState(0)

  return (
    <div className="Dog">
      <h1>PERRO</h1>
      <h2>GUAO GUAO</h2>
    </div>
  )
}

export default Dog
