import shutil
import os
from pathlib import Path

from logic.workspace_management.workspace import workspace
from logic.constants import WorkspaceFolders, FileTransferResults


class FileManager:
    @staticmethod
    def copy_file(source_file_path: str, project_id) -> str | None:
        """
        Copy a file to the StreamQL workspace.

        Args:
            source_file_path: Path of the file to be copied into the workspace.
            project_id: Used for future enhancements or naming separation.

        Returns:
            The path to the copied file (as string) or None if it fails.
        """
        try:
            destination_dir = workspace.get_path(WorkspaceFolders.USER_FILES)
            Path(destination_dir).mkdir(parents=True, exist_ok=True)
            destination_path = Path(destination_dir) / Path(source_file_path).name
            shutil.copy(source_file_path, destination_path)
            return str(destination_path)
        except Exception as e:
            print(f"Error copying file: {e}")
            return None

    @staticmethod
    def delete_file(file_id: str) -> bool:
        """
        Deletes a file from the StreamQL workspace.

        Args:
            file_id: Name of the file to delete.

        Returns:
            True if the file was deleted, False otherwise.
        """
        try:
            file_path = Path(workspace.get_path(WorkspaceFolders.USER_FILES)) / file_id
            if file_path.exists():
                file_path.unlink()
                return True
            else:
                print(f"File not found: {file_path}")
                return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False

    @staticmethod
    def update_file(file_id: str, new_file_path: str) -> FileTransferResults:
        """
        Replace an existing file in the workspace with a new one.

        Args:
            file_id: The name of the file to replace.
            new_file_path: Path to the new file that will overwrite the existing one.

        Returns:
            FileTransferResults indicating success or failure.
        """
        try:
            df = pd.read_csv(file_path, nrows=5)
            return not df.empty and len(df.columns) > 0
        except Exception:
            return False

    @staticmethod
    def get_file(file_id: str) -> Path | None:
        """
        Get the full path to a file in the workspace.

        Args:
            file_id: Name of the file to fetch.

        Returns:
            Path object if the file exists, otherwise None.
        """
        file_path = Path(workspace.get_path(WorkspaceFolders.USER_FILES)) / file_id
        if file_path.exists():
            return file_path
        else:
            print(f"File not found: {file_path}")
            return None


file_manager = FileManager()
