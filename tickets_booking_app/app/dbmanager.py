from pathlib import Path

from sqlalchemy import create_engine, MetaData, Table


class DbManager:
    def __init__(self, file_name):
        self.file_name = file_name

    def _get_path(self):
        path = Path(self.file_name).resolve()
        return path

    def get_db(self):
        db = create_engine(f'sqlite:///{self._get_path()}', echo=True)
        return db

    def get_table(self, table_name: str):
        table = Table(table_name, MetaData(), autoload=True, autoload_with=self.get_db())
        return table
