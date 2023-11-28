from rich import print as rprint
from sqlmodel import SQLModel, create_engine  # noqa: F401

# from models import Hero, Team  # noqa: F401
from models_2 import Hero, HeroTeamLink, Team  # noqa: F401

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)
# engine = create_engine(sqlite_url)

def get_tables():
    rprint(SQLModel.metadata.tables)


def drop_tables():
    SQLModel.metadata.reflect(engine)
    SQLModel.metadata.drop_all(engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)