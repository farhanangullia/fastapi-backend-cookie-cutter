from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.monitoring.log import logger


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.exception(
        exc, extra={"uuid": request.state.correlation_id, "type": "api-error"}
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"uuid": request.state.correlation_id, "message": exc.detail},
    )
