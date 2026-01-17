from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Global exception handler for HTTP exceptions
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail if hasattr(exc, 'detail') else "An HTTP error occurred",
                "details": str(exc)
            }
        }
    )


async def validation_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for validation errors
    """
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation error occurred",
                "details": str(exc)
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for general exceptions
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal error occurred",
                "details": str(exc) if str(exc) else "Unknown error"
            }
        }
    )