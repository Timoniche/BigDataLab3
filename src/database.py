import os
from contextlib import closing

import psycopg2
from psycopg2 import extensions

from logger import Logger


class Database:
    def __init__(self):
        logger = Logger(show=True)
        self.log = logger.get_logger(__name__)

        self.pg_user = os.environ.get('PG_USER')
        self.pg_password = os.environ.get('PG_PASSWORD')
        self.pg_dbname = os.environ.get('PG_DB')

    def execute(
            self,
            command: str,
            args=None,
    ):
        try:
            with closing(
                    # url: jdbc:postgresql://db:5432/{pg_dbname}
                    psycopg2.connect(
                        dbname=self.pg_dbname,
                        user=self.pg_user,
                        password=self.pg_password,
                        # host='localhost',
                        host='db',
                    )
            ) as connection:
                connection.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)

                with connection.cursor() as cursor:
                    if args is None:
                        cursor.execute(command)
                    else:
                        cursor.execute(command, args)

                    if cursor.pgresult_ptr is None:
                        return None

                    return cursor.fetchall()
        except psycopg2.DatabaseError as e:
            self.log.error(f'Psycopg2 db error, error: {e}, command: {command}')


def main():
    db = Database()
    db.execute('SELECT datname FROM pg_database')


if __name__ == '__main__':
    main()
