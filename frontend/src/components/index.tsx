import type React from "react"
import { useState } from "react"

interface HelloWorldProps {
  title: string // 定义组件的 props 类型
  render?: () => React.ReactNode // JSX.Element 只能返回一个element，而 React.ReactNode 可以返回多个元素、字符串、数字等
  render2?: (count:number) => React.ReactNode // 也可以定义带参数的 render props, 将内部状态 count 传递给外部组件
  onChange?: (value: string) => void  // 定义一个可选的 onChange 回调函数，接受一个字符串参数。用来通知外界，里面发生了什么
}

// 具名导出
export const HelloWorld = (props: HelloWorldProps) => {
  const [count, setCount] = useState(0) // 定义一个内部状态 count
  const handleAdd = () => {
    setCount(count + 1)
    props.onChange?.(`count 已经增加到 ${count + 1}`) // 调用 onChange 回调函数，并传递新的 count 值
  }
  
  return (
  <>
  <h1>Hello, {props.title}! {props.render?.()} {props.render2?.(count)} </h1>
    <button onClick={handleAdd}>点击增加 count</button>
  </>)
}




const HelloReact = () => {
  return <h1>Hello, React!</h1>
}
// 默认导出
export default HelloReact 