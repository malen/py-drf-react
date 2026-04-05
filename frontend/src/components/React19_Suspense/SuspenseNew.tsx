import { Suspense, use } from "react";

const Message = ({messagePromise}: {messagePromise: Promise<string>}) => {
  const message = use(messagePromise);
  return <div>Message 组件内容{message}</div>
}

export const SuspenseNew = () => {
  const messagePromise = new Promise<string>((resolve) => {
    setTimeout(() => {
      resolve("这是一个异步加载的消息")
    }, 2000)
  })
  return (
    <>
    <Suspense fallback={<div>Loading...</div>}>
      <Message messagePromise={messagePromise} />
    </Suspense>
    </>
  );
}