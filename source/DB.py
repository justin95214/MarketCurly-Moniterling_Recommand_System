from importlib.metadata import metadata
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table
from xmlrpc.client import DateTime


class DB:
    def __init__(self, table_name, engine_url, ) -> None:
        self.TALBE_NAME = table_name
        self.init_engine(engine_url)
        self.Base = declarative_base()
        self.db_session = scoped_session(sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine))
        self.conn = self.engine.connect()
        self.meta_data = MetaData(bind=self.engine)
        self.table = Table(table_name, self.meta_data, autoload=True)
        self.insert_table = self.table.insert()

    def init_engine(self, engineUrl):
        self.engine = create_engine(engineUrl, convert_unicode=True)

    def init_db(self):
        self.Base.metadata.create_all(self.engine)
        self.Base.query = self.db_session.query_property()

    def insertDB(self, date, title, price, weight, kind, site, location):
        try:
            self.insert_table.execute(
                date=DateTime(date),
                title=str(title),
                price=int(price),
                weight=str(weight),
                kind=str(kind),
                site=str(site),
                location=str(location)
            )
            print(f'%%\t{self.TALBE_NAME}\tDB INSERT {date}')
        except IntegrityError as e:
            pass

    def get_conn(self):
        return self.conn
