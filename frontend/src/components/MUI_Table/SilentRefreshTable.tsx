import { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

export default function SilentRefreshTable() {
  // 1. 表格数据存在 state 中
  const [data, setData] = useState([
    { id: 1, name: '张三', age: 28 },
    { id: 2, name: '李四', age: 32 },
  ]);

  // 2. 模拟定时/触发式数据更新（无感刷新）
  useEffect(() => {
    const timer = setInterval(() => {
      setData(prev => prev.map(item => 
        item.id === 1 ? { ...item, age: item.age + 1 } : item
      ));
    }, 2000);
    return () => clearInterval(timer);
  }, []);

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>姓名</TableCell>
            <TableCell>年龄</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {/* 3. 数据变化时，仅更新对应行/单元格，无闪烁 */}
          {data.map((row) => (
            <TableRow key={row.id}>
              <TableCell>{row.name}</TableCell>
              <TableCell>{row.age}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}