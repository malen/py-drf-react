from rest_framework.views import exception_handler as drf_exception_handler


def success_response(data=None, message="Success", status_code=200):
    """
    生成一个成功的响应对象
    :param data: 响应数据，默认为 None
    :param message: 响应消息，默认为 "Success"
    :param status_code: HTTP 状态码，默认为 200
    :return: 包含 success、message 和 data 的字典
    """
    return {
        "success": True,
        "message": message,
        "data": data,
        "status_code": status_code,
    }


def error_response(message="Error", status_code=400, data=None):
    """
    生成一个错误的响应对象
    :param message: 错误消息，默认为 "Error"
    :param status_code: HTTP 状态码，默认为 400
    :param data: 可选的错误数据，默认为 None
    :return: 包含 success、message 和 data 的字典
    """
    return {
        "success": False,
        "message": message,
        "data": data,
        "status_code": status_code,
    }


def exception_handler(exception, context):
    """
    生成一个异常的响应对象
    :param exception: 异常对象
    :param status_code: HTTP 状态码，默认为 500
    :return: 包含 success、message 和 data 的字典
    """
    res = drf_exception_handler(
        exception, context
    )  # 调用 DRF 的默认异常处理器获取响应对象
    if res is not None:
        status_code = (
            res.status_code
        )  # 如果 DRF 处理器返回了响应对象，则使用其中的状态码

    return {
        "success": False,
        "message": str(exception),
        "data": None,
        "status_code": status_code,
    }
