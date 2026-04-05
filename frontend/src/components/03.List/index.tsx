import { useState } from "react"

export const List = () => {
  const [list, setList] = useState<string[]>(["列表项 1", "列表项 2", "列表项 3"])
  return (
    <div>
      <button onClick={() => setList([...list, `列表项 ${list.length + 1}`])}>添加列表项</button>
      {list.map((item, index) => (
        <p key={index}>
        {/* 这里使用 index 作为 key 是不推荐的，因为如果列表项发生变化，React 可能无法正确识别哪些项被修改了，从而导致性能问题和潜在的 bug。建议使用一个唯一的标识符作为 key，比如列表项的 id 或者内容本身（如果内容是唯一的）。 */
        }
        {item}</p>
      ))}
    </div> 
  )
}