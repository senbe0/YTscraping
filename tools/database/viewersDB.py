from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoSuchTableError
import os


database_path = os.path.join(os.path.dirname(__file__), "YTviewers.db") 
db_path = f"sqlite:///{database_path}"

engine = create_engine(db_path, echo=True)
Session = sessionmaker(bind=engine)
metadata = MetaData()


def create_table(table_name):
    table = Table(table_name, metadata,
        Column("sequence", Integer, primary_key=True),
        Column("time", String),
        Column("viewers", Integer),
    )

    metadata.create_all(engine)

def delete_viewerTable(table_name):
    try:
        table = Table(table_name, metadata, autoload_with=engine)
        table.drop(engine)
    except NoSuchTableError:
        pass

def insert_viewerRecord(table_name, db_time: str, db_viewers: int):
    table = Table(table_name, metadata, autoload_with=engine)

    session = Session()

    try:
        ins = table.insert().values(time=db_time, viewers=db_viewers)
        session.execute(ins)

        session.commit()

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()
