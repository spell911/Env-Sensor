import psycopg2

from config import config


def create_tables():
    """ create tables in the PostgreSQL database

    """

    commands = [
        """
        CREATE TABLE IF NOT EXISTS iot_telemetry (
            env_id SERIAL PRIMARY KEY,
            ts REAL NOT NULL,
            device CHAR(17) NOT NULL,
            co DOUBLE PRECISION,
            humidity DOUBLE PRECISION,
            light SMALLINT,
            lpg DOUBLE PRECISION,
            motion SMALLINT,
            smoke DOUBLE PRECISION,
            temp DOUBLE PRECISION
        )
        """,
        """CREATE TABLE IF NOT EXISTS device_00 (
            device_00_id SERIAL PRIMARY KEY,
            ts DOUBLE PRECISION NOT NULL,
            device CHAR(17) NOT NULL,
            co DOUBLE PRECISION,
            humidity DOUBLE PRECISION,
            light BOOLEAN,
            lpg DOUBLE PRECISION,
            motion BOOLEAN,
            smoke DOUBLE PRECISION,
            temp DOUBLE PRECISION
        )""",
        """CREATE TABLE IF NOT EXISTS device_1c (
            device_1c_id SERIAL PRIMARY KEY,
            ts DOUBLE PRECISION NOT NULL,
            device CHAR(17) NOT NULL,
            co DOUBLE PRECISION,
            humidity DOUBLE PRECISION,
            light BOOLEAN,
            lpg DOUBLE PRECISION,
            motion BOOLEAN,
            smoke DOUBLE PRECISION,
            temp DOUBLE PRECISION
        )""",
        """CREATE TABLE IF NOT EXISTS device_b8 (
            device_b8_id SERIAL PRIMARY KEY,
            ts DOUBLE PRECISION NOT NULL,
            device CHAR(17) NOT NULL,
            co DOUBLE PRECISION,
            humidity DOUBLE PRECISION,
            light BOOLEAN,
            lpg DOUBLE PRECISION,
            motion BOOLEAN,
            smoke DOUBLE PRECISION,
            temp DOUBLE PRECISION
        )"""]
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            # print(command)
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
