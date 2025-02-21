import sqlite3
import os
from pathlib import Path


class DB:
    @staticmethod
    def create_db(db_name: str, workspace_path: str) -> sqlite3.Connection:
        """
        Creates a new SQLite database file if it doesn't exist.
        Returns a connection to the database.

        Args:
            db_name (str): Name of the database file (e.g., 'mydb.db').
            workspace_path (str): Path to the directory where the DB should be located.

        Returns:
            sqlite3.Connection: Connection object to the SQLite database.
        """
        workspace = Path(workspace_path)
        workspace.mkdir(parents=True, exist_ok=True)

        db_path = workspace / db_name
        conn = sqlite3.connect(db_path)
        return conn

    @staticmethod
    def delete_db(db_name: str, workspace_path: str):
        """
        Deletes the SQLite database file if it exists.

        Args:
            db_name (str): Name of the database file to delete.
            workspace_path (str): Path to the directory where the DB is located.
        """
        db_path = Path(workspace_path) / db_name
        if db_path.exists():
            db_path.unlink()


db = DB()
