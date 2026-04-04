from rest_framework.pagination import PageNumberPagination, Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # 每页默认显示的条数
    page_size_query_param = "size"  # 前端可以通过这个参数来指定每页显示的条数
    max_page_size = 100  # 每页最大显示的条数
    page_query_param = "page"  # 前端可以通过这个参数来指定页码


# 返回统一格式的分页响应
class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"
    max_page_size = 50
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response(
            {
                "success": True,
                "message": "Success",
                "data": {
                    "count": self.page.paginator.count,  # 总条数
                    "total_pages": self.page.paginator.num_pages,  # 总页数
                    "current_page": self.page.number,  # 当前页码
                    "results": data,  # 当前页的数据列表
                },
                "status_code": 200,
            }
        )
