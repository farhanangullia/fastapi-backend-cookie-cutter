import uuid
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from mangum import Mangum

from app.routes import root, user
from app.monitoring import log
from app.monitoring.log import logger
from app.middlewares.coid import CorrelationIdMiddleware
from app.middlewares.logging import LoggingMiddleware
from app.handlers.exception_handler import exception_handler
from app.handlers.http_exception_handler import http_exception_handler
from app.utilities.settings import settings
from fastapi.middleware.cors import CORSMiddleware
from app.domain.repository.user_repository import UserRepository


###############################################################################
#   Startup dependencies                                                     #
###############################################################################


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        UserRepository()
    except Exception as e:
        logger.exception(e)
        raise e
    yield
    log.info("Shutting down...")


###############################################################################
#   Application object                                                        #
###############################################################################

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG, lifespan=lifespan)

###############################################################################
#   Logging configuration                                                     #
###############################################################################

log.configure_logging(
    level=settings.LOG_LEVEL, service=settings.APP_NAME, instance=str(uuid.uuid4())
)

###############################################################################
#   Error handlers configuration                                              #
###############################################################################

app.add_exception_handler(Exception, exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

###############################################################################
#   Middlewares configuration                                                 #
###############################################################################

# Tip : middleware order : CorrelationIdMiddleware > LoggingMiddleware -> reverse order
app.add_middleware(LoggingMiddleware)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

###############################################################################
#   Routers configuration                                                     #
###############################################################################

app.include_router(
    root.router,
    tags=["base"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    user.router,
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


###############################################################################
#   Handler for AWS Lambda                                                    #
###############################################################################

handler = Mangum(app)

logger.info("Started app...")

###############################################################################
#   Run the self contained application                                        #
###############################################################################

if __name__ == "__main__":
    logger.info("Starting through main...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
