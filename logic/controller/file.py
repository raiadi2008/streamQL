from uuid import UUID, uuid4 as uuid
import csv
import pandas as pd

from logic.workspace_management.file_manager import file_manager


class FileController:
    def __init__(self):
        pass

    @staticmethod
    def validate_csv_file(source_file_path: str, sample_lines=10) -> bool:
        """
        validates if the given file is a csv or not
        Args:
            source_file_path: Path of the file to be validated
        Return:
            Bool True if file is CSV and valid and False if not
        """
        try:
            df = pd.read_csv(source_file_path, nrows=sample_lines)
            return not df.empty and len(df.columns) > 0
        except Exception:
            return False

    def add_file(self, source_file_path: str, project_id: UUID):
        """
        Adds a file to stream ql project
        Add the csv file to the database of project
        Args:
            source_file_path: Path of the file to be copied
            project_id: Id of the project in which file is to be added
        """
        if not self.validate_csv_file(source_file_path=source_file_path):
            return "File is not CSV"
        file_uniqe_id = uuid()
        file_manager.copy_file(source_file_path=source_file_path)
        
