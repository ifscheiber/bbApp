from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import DeclarativeBase

from db_connections.DB_CONN import DATABASE_CONNECTOR


class Base(DeclarativeBase):

    schema = "LEAPNODE_USER_MGMT"

    def delete_table(self, db: DATABASE_CONNECTOR, tablename: str): 
        conn = db.get_conn('PG_GAM')

        # execute the DROP TABLE command
        conn.execute(text(f"DROP TABLE IF EXISTS {tablename} CASCADE;"))

        # commit the transaction
        conn.commit()
