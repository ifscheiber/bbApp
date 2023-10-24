from db_connections.DB_CONN import DATABASE_CONNECTOR
from sqlalchemy.orm import sessionmaker, scoped_session


def query_db(session, object_class):
    mapped_object: object_class = session.query(object_class).all()
    return mapped_object


database_str = 'PG_GAM'
DBConnection = DATABASE_CONNECTOR([database_str])
ScopedSession = scoped_session(sessionmaker(bind=DBConnection.get_engine(database_str)))