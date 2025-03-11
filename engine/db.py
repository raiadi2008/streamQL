import sqlite3
import os
from pathlib import Path
from typing import Any, List, Tuple, Optional


class EngineDB:
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

    @staticmethod
    def execute_query(
        sql_query: str,
        db_name: str,
        workspace_path: str,
        params: Optional[Tuple[Any, ...]] = None,
        fetch: bool = True,
    ) -> Optional[List[Tuple[Any, ...]]]:
        """
        Executes a query on the given SQLite database.

        Args:
            sql_query (str): SQL query to execute.
            db_name (str): Name of the SQLite database.
            workspace_path (str): Path where the database is stored.
            params (Tuple[Any, ...], optional): Parameters for parameterized query.
            fetch (bool): If True, fetch results for SELECT queries.

        Returns:
            Optional[List[Tuple]]: Result of SELECT query, or None for others.
        """
        db_path = Path(workspace_path) / db_name
        if not db_path.exists():
            raise FileNotFoundError(f"Database not found at {db_path}")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            if params:
                cursor.execute(sql_query, params)
            else:
                cursor.execute(sql_query)

            if fetch and sql_query.strip().lower().startswith("select"):
                result = cursor.fetchall()
            else:
                result = None
                conn.commit()
        finally:
            cursor.close()
            conn.close()

        return result
