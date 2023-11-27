from sqlmodel import SQLModel, create_engine
from models import Team, Hero   # noqa: F401

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)
# engine = create_engine(sqlite_url)
