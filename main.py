from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import uvicorn
from starlette.staticfiles import StaticFiles

from task import router as task_router
from account import router as account_router
from address import router as address_router
from theme import router as theme_router
from collections import defaultdict

app = FastAPI(title="Address Book App",
    docs_url="/address-book-docs",
    version="0.0.1")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    reformatted_message = defaultdict(list)
    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        field_string = ".".join(filtered_loc)  # nested fields with dot-notation
        reformatted_message[field_string].append(msg)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "Errors": reformatted_message}),
    )

@app.get("/")
async def root():
    return {"message": "Hello Address Book API"}


app.include_router(task_router.router)
app.include_router(account_router.router)
app.include_router(theme_router.router)
app.include_router(address_router.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)