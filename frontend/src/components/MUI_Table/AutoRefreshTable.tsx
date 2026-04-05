import { useState, useEffect } from 'react';
import {
  Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Paper, Button
} from '@mui/material';

export default function AutoRefreshTable() {
  const [data, setData] = useState([]);

  // 👉 从 API 获取最新数据（可能增加、减少、修改）
  const fetchLatestData = async () => {
    try {
      // 真实项目替换成你的接口：
      // const res = await fetch('/api/list');
      // const newData = await res.json();

      // 模拟：每次返回的数据**可能变多**
      const newData = [
        { id: 1, name: '张三' },
        { id: 2, name: '李四' },
        ...(Math.random() > 0.5 ? [{ id: Date.now(), name: '新增记录' }] : []),
      ];

      // ✅ 关键：直接覆盖，不是追加！
      setData(newData);
    } catch (err) {}
  };

  // 初始加载
  useEffect(() => {
    // ✅ 立即执行一次（刚进页面就加载数据）
    // 定义一个异步函数
    const init = async () => {
        await fetchLatestData(); // 立即加载数据
    };

    init(); // 立即执行

    const timer = setInterval(fetchLatestData, 2000); // 每 2 秒自动刷新一次
    return () => clearInterval(timer); // 组件卸载时清除定时器
  }, []);

  return (
    <TableContainer component={Paper} sx={{ margin: 2 }}>
      {/* 手动刷新按钮 */}
      <Button onClick={fetchLatestData} sx={{ m: 2 }}>
        刷新 API 数据（可能新增记录）
      </Button>

      <Table>
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>姓名</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {/* 👉 key 必须唯一，React 才能无感 diff */}
          {data.map((row) => (
            <TableRow key={row.id}>
              <TableCell>{row.id}</TableCell>
              <TableCell>{row.name}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}