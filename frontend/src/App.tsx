
import { useState } from 'react'

import { HelloWorld } from './components'
import { List } from './components/03.List'
import { Hooks } from './components/04.Hooks'

function App() {
  const [count, setCount] = useState(0)
  return (
    <>
    {/* <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>
        Click me
      </button>
    </div>
    <HelloWorld title="My App" render={()=><div>render props 有点像插槽</div>}
    render2={(count:number) => <p>显示内部状态count{count}</p>} onChange={(value) => console.log(value)} />

    <List /> */}

    <Hooks />
    </>
  )
}

export default App
