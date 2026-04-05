# 创建React项目
pnpm create vite

# 创建组件 推荐函数式组件
## 函数式组件和Hooks 成为现代React开发的标准。
function App() {
    return <div></div>;
}
## 类组件写法太啰嗦
<!-- class App extends React.Component {
    render() {
        return <div></div>;
    }
} -->

## Props 与组件通信
这里的render 和 render2 与 onChange 在函数签名上很像，但本质不一样。
render 和 render2 更像Vue3中的插槽，用来渲染UI。
而onChange 是事件，返回值为void，用来处理副作用。
```jsx
// 父组件
    <HelloWorld title="My App" render={()=><div>render props 有点像插槽</div>}
    render2={(count:number) => <p>显示内部状态count{count}</p>} onChange={(value) => console.log(value)} />

// 子组件
interface HelloWorldProps {
  title: string // 定义组件的 props 类型
  render?: () => React.ReactNode // JSX.Element 只能返回一个element，而 React.ReactNode 可以返回多个元素、字符串、数字等
  render2?: (count:number) => React.ReactNode // 也可以定义带参数的 render props, 将内部状态 count 传递给外部组件
  onChange?: (value: string) => void  // 定义一个可选的 onChange 回调函数，接受一个字符串参数。用来通知外界，里面发生了什么
}

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
  </>
  )
}
```

## 状态管理
const [count setCount] = useState(0);

如果是复杂对象
const [info, setInfo] = useState({age: 0});

更新状态的时候，推荐下面写法
setInfo((prevInfo) => {
    ...prevInfo,
    age: prevInfo.age + 1,
})

## Hooks

### useState
```jsx
  useEffect(() => {
    console.log("count 发生变化了", count)
    document.title = `当前 count: ${count}` // 每当 count 发生变化时，更新页面标题
  }, [count]) // 依赖项是 count，当 count 发生变化时，useEffect 内的函数会被调用

  useEffect(() => {
    console.log("组件挂载了")

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
```

### useRef
有两种用法
1. 引用DOM元素
```jsx
const inputRef = useRef<HTMLInputElement>(null) // 定义一个 ref，用来获取 input 元素的引用

useEffect(() => {
    inputRef.current?.focus() // 组件挂载后自动聚焦到 input 元素
}, []);
return (
    <>
    <input ref={inputRef} placeholder="输入内容后点击按钮获取值" />
    </>
)
```

2. 持有非状态数据
```jsx
const data = useRef(false);
```

## React19 新特性
