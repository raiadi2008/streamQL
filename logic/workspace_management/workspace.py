from pathlib import Path
from logic.constants import WorkspaceFolders


class Workspace:
    def __init__(self, base_dir: Path | None = None):
        """Container for all files created by StreamQL.

        Parameters
        ----------
        base_dir: optional :class:`~pathlib.Path`
            Base directory for the workspace.  Defaults to ``~/streamql``.
        """
        self.workspace_path = base_dir or (Path.home() / "streamql")
        self.paths: dict[str, Path] = {}

    def create_workspace(self):
        """Create the directory tree used by the application."""
        self.workspace_path.mkdir(parents=True, exist_ok=True)

        for folder in WorkspaceFolders:
            folder_path = self.workspace_path / folder.value
            folder_path.mkdir(parents=True, exist_ok=True)
            self.paths[folder.name.lower()] = folder_path

    def get_path(self, folder: WorkspaceFolders) -> Path:
        return self.paths.get(folder.name.lower())


workspace = Workspace()
