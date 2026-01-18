"""HTTP logging middleware.

This middleware logs structured entries starting with:
- timestamp
- path
- HttpMethodInvoked
- logrequiredFieldsfromPayload (payload body if JSON-parsable)

It aligns to the logging requirements described in the README.
"""

import logging
from datetime import datetime
from fastapi import Request

logger = logging.getLogger("movieflix")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

async def logging_middleware(request: Request, call_next):
    """Log request metadata and payload before passing to the next handler."""
    body = None
    try:
        body = await request.json()
    except Exception:
        body = {}
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "path": request.url.path,
        "HttpMethodInvoked": request.method,
        "logrequiredFieldsfromPayload": body,
    }
    logger.info(log_entry)
    response = await call_next(request)
    return response
