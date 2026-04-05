import { useEffect, useRef, useState } from "react"


export const Hooks = () => {
  const [count, setCount] = useState(0)

  function handleAdd() {
    // setTimeout(() => {
    //   setCount(count + 1) // 这里的 count 是闭包中的值，永远是初始值 0，所以每次点击只会增加到 1
    //   setCount(count + 1)
    //   setCount(count + 1)
    // }, 1000)
    setCount((c) => c + 1) // 推荐使用函数式更新，避免闭包问题
  }

  useEffect(() => {
    console.log("count 发生变化了", count)
    document.title = `当前 count: ${count}` // 每当 count 发生变化时，更新页面标题
  }, [count]) // 依赖项是 count，当 count 发生变化时，useEffect 内的函数会被调用

  useEffect(() => {
    console.log("组件挂载了")

    inputRef.current?.focus() // 组件挂载后自动聚焦到 input 元素

    // 模拟订阅一个事件，比如 WebSocket、定时器等
    const timer = setInterval(() => {
      console.log("定时器触发了")
    }, 1000)
    return () => {
      console.log("组件卸载了") // 组件卸载时执行的清理函数，可以用来取消订阅、清除定时器等
      clearInterval(timer)
    }
  }, []) // 空依赖数组，表示这个 useEffect 只在组件挂载和卸载时执行

  useEffect(() => {
    console.log("组件更新了")
  }) // 没有依赖数组，表示这个 useEffect 在每次组件更新后都会执行


  const inputRef = useRef<HTMLInputElement>(null) // 定义一个 ref，用来获取 input 元素的引用
  return (
      <>
      <div>Hooks</div><button onClick={handleAdd}>点击增加 count</button><p>当前 count: {count}</p>
      <input ref={inputRef} placeholder="输入内容后点击按钮获取值" />
      </>
  )

}
