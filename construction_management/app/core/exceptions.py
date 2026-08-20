from fastapi import Request, HTTPException, status
from datetime import datetime
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def register_exception_handlers(app):
    """
    Đăng ký global exception handlers cho FastAPI app
    Các lỗi sẽ được xử lý và trả response định dạng thống nhất
    """

    # =========================================================
    # 422 - VALIDATION ERROR
    # =========================================================
    
    def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        Xử lý lỗi validation (dữ liệu sai định dạng)
        VD: gửi email không đúng format, missing required field,...
        """
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "success": False,
                "status_code": 422,
                "message": "Dữ liệu gửi lên không đúng định dạng",
                "path": request.url.path,
                "timestamp": datetime.now().isoformat(),
                "detail": exc.errors(),  # Chi tiết lỗi validation
            },
        )

    # =========================================================
    # 4xx & 5xx - HTTP EXCEPTION
    # =========================================================
    
    def http_exception_handler(request: Request, exc: HTTPException):
        """
        Xử lý HTTPException (401, 403, 404, 500,...)
        VD: token sai, không có quyền, resource không tìm thấy,...
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "status_code": exc.status_code,
                "message": exc.detail,
                "path": request.url.path,
                "timestamp": datetime.now().isoformat(),
                "detail": None,
            },
        )

    # =========================================================
    # 500 - GENERAL EXCEPTION
    # =========================================================
    
    def general_exception_handler(request: Request, exc: Exception):
        """
        Xử lý các exception không lường trước
        Trả lỗi 500 chung chung để không lộ chi tiết lỗi ra client
        """
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "status_code": 500,
                "message": "Lỗi máy chủ nội bộ. Vui lòng thử lại sau.",
                "path": request.url.path,
                "timestamp": datetime.now().isoformat(),
                "detail": None,
            },
        )

    # Đăng ký các handlers với FastAPI
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
