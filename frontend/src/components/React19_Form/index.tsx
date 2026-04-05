import { useActionState, useState } from "react";
import { useFormStatus } from "react-dom";

export const OldForm = () => {
  const [formData, setFormData] = useState<{ name: string }>({
    name: ""
  });
  const handleSubmit = (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault() // 阻止表单默认提交行为，避免页面刷新
    const formData2 = new FormData(e.currentTarget) // 获取表单数据
    const name = formData2.get("name") // 获取 name 字段的值
    alert(`提交的名字是: ${name}`) // 显示提交的名字

    console.log("formData", formData) // 这里的 formData 是 useState 中的状态值，初始值是 { name: "" }，所以每次提交时都会显示这个初始值。因为 handleSubmit 函数中的 formData 是闭包中的值，它不会随着输入框的变化而更新。要想在提交时获取最新的输入值，可以直接从事件对象 e.currentTarget 中获取表单数据，而不是依赖于 useState 中的状态值。或者可以在输入框的 onChange 事件中更新 useState 中的状态值，这样在提交时就可以使用最新的状态值了。
  }
  
  return (
    <form onSubmit={handleSubmit}>
        <label htmlFor="name">Name:</label>
        <input type="text" id="name" name="name" value={formData.name} onChange={(e) => setFormData({...formData, name: e.target.value})} />
        <button type="submit">Submit</button>
    </form>
  );
}


export const NewForm = () => {
  const handleActon = (formData: FormData) => {
    console.log("formData", formData.get("name")) // 直接从 formData 中获取 name 字段的值
  }
  
  return (
    <form action={handleActon}>
        <label htmlFor="name">Name:</label>
        <input type="text" id="name" name="name" />
        <button type="submit">Submit</button>
    </form>
  );
}

// 模拟一个异步操作，比如网络请求等，返回一个 Promise 对象，在指定的时间后 resolve。
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms)) 

interface ActionState {
  success: boolean
}
const SubmitButton = () => {
    // useFormStatus在子组件中，可以获取所在Form表单的提交状态。当表单提交时，pending 会变为 true，直到提交完成后才会变回 false。data 是 handleActon 函数返回的新状态值，可以在提交完成后获取到这个值。 method 是表单提交的 HTTP 方法，比如 "POST"、"GET" 等，可以根据需要进行不同的处理。
    const {pending, data, method} = useFormStatus();
    return <button type="submit">{pending ? "Submitting..." : "Submit"}</button>
};

// 通过useActionState获取提交的状态
export const NewForm2 = () => {
  const handleActon = async (prevSate: ActionState | null, formData: FormData) => {
    console.log("formData", formData.get("name")) // 直接从 formData 中获取 name 字段的值
    await delay(2000) // 模拟一个异步操作，等待 2 秒钟

    return {success: true} // 返回新的状态值，这个值会被 useActionState 接收并更新组件的状态
  }
  
  const [state, submitAction, isPending] = useActionState(handleActon, null) // useActionState 接收一个函数，这个函数会在表单提交时被调用，并且接收两个参数：prevState 是当前的状态值，formData 是提交的表单数据。useActionState 会返回一个状态值 state 和一个函数 setState，用来更新这个状态值。当表单提交时，handleActon 函数会被调用，并且 formData 中包含了提交的表单数据，我们可以直接从 formData 中获取 name 字段的值，而不需要依赖于 useState 中的状态值。

  console.log("state", state) // 这里的 state 是 useActionState 中的状态值，初始值是 null，每次提交时都会被 handleActon 函数更新为 handleActon 返回的新状态值。
  console.log("isPending", isPending) // isPending 是一个布尔值，表示表单提交是否正在进行中。当表单提交时，isPending 会变为 true，直到 handleActon 函数执行完成后才会变回 false.

  return (
    <form action={submitAction}>
        <label htmlFor="name">Name:</label>
        <input type="text" id="name" name="name" />
        <SubmitButton />
    </form>
  );
}