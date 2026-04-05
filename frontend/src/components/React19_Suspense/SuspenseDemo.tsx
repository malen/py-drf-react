import { lazy, Suspense } from "react";
// import { Child } from "./Child";

const LazyChild = lazy(() => import("./Child")) // 使用 React.lazy 动态导入 Child 组件，只有在 Suspense 组件内使用时才会加载 Child 组件的代码
export const SuspenseDemo = () => {
  return (
    <>
      <div>SuspenseDemo 组件内容</div>
      <Suspense fallback={<div>Loading...</div>}>
        <LazyChild /> {/* 在 Suspense 组件内使用 LazyChild 组件，当 LazyChild 组件正在加载时，会显示 fallback 中的内容 */}
      </Suspense>
    </>
  );
}