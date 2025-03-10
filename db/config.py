from sqlmodel import SQLModel, create_engine, Session

class Config:
    ENGINE = create_engine("sqlite:///my_db.db", echo=True)
    SESSION = Session(bind=ENGINE)


    @classmethod
    def migrate(cls):
        SQLModel.metadata.drop_all(cls.ENGINE)
        SQLModel.metadata.create_all(cls.ENGINE)