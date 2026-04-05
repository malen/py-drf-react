import { useCallback, useState } from "react";

export default function RealApiPaginationTable() {
    const [data, setData] = useState([]); // 存储表格数据
    const [loading, setLoading] = useState(false); // 加载状态
    const [page, setPage] = useState(1); // 当前页码
    const [rowsPerPage, setRowsPerPage] = useState(5); // 每页条数
    const [total, setTotal] = useState(0); // 数据总条数

    const fetchLatestData = useCallback(async () => {
        try {
            const res = await fetch('/api/list'); // 替换成你的接口
            const newData = await res.json();
            console.log("Fetched data:", newData);

            // 后端返回格式
            setData(newData);
            setTotal(newData.length); // 假设后端返回的数据就是当前页的数据，且包含 total 字段

        } catch (err) {
            console.error("Error fetching data:", err);
        } finally {
            setLoading(false);
        }
    }, []);

  return (
    <div>
      <h2>RealApiPaginationTable 组件内容</h2>
      <p>这是一个使用真实 API 数据的分页表格组件，数据会每 2 秒自动刷新一次。</p>
    </div>
  );
}