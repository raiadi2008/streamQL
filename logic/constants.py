from enum import Enum


class WorkspaceFolders(Enum):
    USER_FILES = "user-files"
    LOGS = ".logs"
    QUERIES = "queries"
    STORES = "stores"
    PROJECTS = "projects"


class FileTransferResults(Enum):
    COPY_SUCCESS = "copy_success"
    COPY_FAILED = "copy_failed"
    DELETE_SUCCESS = "delete_success"
    DELETE_FAILED = "delete_failed"


STREAMQL_STORE = "streamql_store"
