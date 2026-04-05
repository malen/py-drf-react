import { useState, useEffect, useCallback } from 'react';
import {
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
  TablePagination, Paper, Box, Typography
} from '@mui/material';
interface Record {
  id: number;
  content: string;
}
export default function PaginationSilentTable() {
  const [data, setData] = useState<Record[]>([]);
  const [loading, setLoading] = useState(false);

  // -------------- 分页 --------------
  const [page, setPage] = useState<number>(1); // 🢂 默认停在【第二页】！
  const [rowsPerPage, setRowsPerPage] = useState(5); // 每页5条，方便测试
  const [total, setTotal] = useState(0);

  // 模拟全局数据（真实项目由后端返回）
  const [allRecords, setAllRecords] = useState<Record[]>([
    { id: 1, content: "历史记录 1" },
    { id: 2, content: "历史记录 2" },
    { id: 3, content: "历史记录 3" },
    { id: 4, content: "历史记录 4" },
    { id: 5, content: "历史记录 5" },
    { id: 6, content: "历史记录 6" },
    { id: 7, content: "历史记录 7" },
    { id: 8, content: "历史记录 8" },
    { id: 9, content: "历史记录 9" },
    { id: 10, content: "历史记录 10" },
  ]);

  // ==============================================
  // 核心：获取【当前分页】的数据（自动处理新增记录）
  // ==============================================
//   const fetchLatestData = async () => {
//     setLoading(true);
//     try {
//       // 后端真实逻辑：offset = 跳过前面的条数
//       const offset = page * rowsPerPage;
//       const currentPageData = allRecords.slice(offset, offset + rowsPerPage);

//       setData(currentPageData);
//       setTotal(allRecords.length);
//     } catch (err) {
//       console.error(err);
//     } finally {
//       setLoading(false);
//     }
//   };
  // 用 useCallback 包裹，保证函数引用不变
const fetchLatestData = useCallback(async () => {
  setLoading(true);
  try {
    const offset = page * rowsPerPage;
    const currentPageData = allRecords.slice(offset, offset + rowsPerPage);

    setData(currentPageData);
    setTotal(allRecords.length);
  } catch (err) {
    console.error(err);
  } finally {
    setLoading(false);
  }
}, [page, rowsPerPage, allRecords]); // 依赖放这里


  // ==============================================
  // 自动新增一条（模拟新记录插入到第一页顶部）
  // ==============================================
  useEffect(() => {
    const addTimer = setInterval(() => {
      setAllRecords(prev => [
        { id: Date.now(), content: `🆕 新插入记录 ${new Date().toLocaleString()}` },
        ...prev
      ]);
    }, 3000);

    return () => clearInterval(addTimer);
  }, []);


  // ==============================================
  // 无感刷新：自动获取当前页最新数据
  // ==============================================
  useEffect(() => {
    // 立即加载
    fetchLatestData();

    // 2秒刷新一次当前页
    const refreshTimer = setInterval(fetchLatestData, 2000);
    return () => clearInterval(refreshTimer);
  }, [fetchLatestData]);

  // 分页事件
  const handleChangePage = (_: React.MouseEvent<HTMLButtonElement> | null, newPage: number) => setPage(newPage);
  const handleChangeRowsPerPage = (e: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(+e.target.value);
    setPage(0);
  };

  return (
    <TableContainer component={Paper} sx={{ margin: 3 }}>
      <Box sx={{ p: 2 }}>
        <Typography variant="h6">
          当前在第 {page + 1} 页（新增记录会挤动分页！）
        </Typography>
      </Box>

      <Table>
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>记录内容</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((row) => (
            <TableRow key={row.id}>
              <TableCell>{row.id}</TableCell>
              <TableCell>{row.content}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <TablePagination
        component="div"
        count={total}
        page={page}
        onPageChange={handleChangePage}
        rowsPerPage={rowsPerPage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </TableContainer>
  );
}