import os
from pathlib import Path
from constants import WorkspaceFolders


class Workspace:
    def __init__(self, username=os.getlogin()):
        self.workspace_path = Path(f"/Users/{username}/streamql")
        self.paths = {}

    def create_workspace(self):
        """
        Creates all the necessary directories to run the application
        """
        # Create main workspace directory
        self.workspace_path.mkdir(exist_ok=True)

        # Create subdirectories and store their paths
        for folder in WorkspaceFolders:
            folder_path = self.workspace_path / folder.value
            folder_path.mkdir(exist_ok=True)
            self.paths[folder.name.lower()] = folder_path

    def get_path(self, folder: WorkspaceFolders) -> Path:
        return self.paths.get(folder.name.lower())


workspace = Workspace()
