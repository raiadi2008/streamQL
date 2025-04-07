from fastapi import FastAPI
from contextlib import asynccontextmanager

from logic.workspace_management.workspace import workspace
from engine.db import EngineDB
from logic.constants import STREAMQL_STORE, WorkspaceFolders
from logic.routers.file import router as file_router
from logic.routers.project import router as project_router
from logic.db.init_db import sqldb


@asynccontextmanager
async def lifespan(app: FastAPI):
    workspace.create_workspace()
    sqldb.init()
    EngineDB.create_db(STREAMQL_STORE, workspace.get_path(WorkspaceFolders.STORES))
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(file_router, prefix="/file")
app.include_router(project_router, prefix="/project")
