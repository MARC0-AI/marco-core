from fastapi import FastAPI

from marco.api.approvals import router as approvals_router

app = FastAPI(title="MARCO Core")

app.include_router(approvals_router)
