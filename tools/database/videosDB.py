from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os


database_path = os.path.join(os.path.dirname(__file__), "YTvideos.db") 
db_path = f"sqlite:///{database_path}"

engine = create_engine(db_path, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class VideoRecord(Base):
    __tablename__ = "video_records"

    videoID = Column(String, primary_key=True)
    channelID = Column(String)
    title = Column(String)
    videoURL = Column(String)
    IconImageURL = Column(String)


def create_table():
    Base.metadata.create_all(engine)


def insert_videoRecord(db_videoID, db_channelID, db_title, db_videoURL, db_iconImageURL):
    session = Session()

    try:
        video_record = VideoRecord(
            videoID=db_videoID,
            channelID=db_channelID,
            title=db_title,
            videoURL=db_videoURL,
            IconImageURL=db_iconImageURL)
        session.add(video_record)
        session.commit()

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def delete__videoRecord(db_videoID: str):
    session = Session()

    try:
        video =session.query(VideoRecord).filter_by(videoID=db_videoID).first()
        session.delete(video)
        session.commit()

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def update_iconImageURL(videoID: str, iconImageURL: str):
    session = Session()

    try:
        video = session.query(VideoRecord).filter_by(videoID=videoID).first()
        video.IconImageURL = iconImageURL
        session.commit()

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()



if __name__ == "__main__":
    # if NOT exist table, create it.
    create_table()
