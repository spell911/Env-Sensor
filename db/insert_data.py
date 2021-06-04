import psycopg2

from .config import config


def insert_data(table, data):
    """ Insert the instance data into table.

    Args:
        table (str): The table we want to insert the data.
        data (dict): The data we want to insert to the table.

    Returns:
        int, SERIAL of rows we inserted.
    Except:
        DatabaseError: database connected, data inserted.
    """
    # get columns name by keys
    columns = list(data.keys())
    # print("\nkeys:", columns)
    # get rows values by values
    rows = list(data.values())
    #print("\nvalues:", rows)

    # returning env_id / SERIAL of rows we inserted.
    sql_insert = "INSERT INTO {table}({columns})\nVALUES {values};"

    conn = None
    env_id = None

    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql_insert.format(table=table, columns=', '.join(
            columns), values=tuple(rows)))
        # get the generated id back
        #env_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    pass
    # return env_id


if __name__ == '__main__':
    # testing
    test_data = {'ts': 1594512094.3859746, 'device': 'b8:27:eb:bf:9d:51', 'co': 0.0049559386, 'humidity': 51.0,
                 'light': False, 'lpg': 0.0076508223, 'motion': False, 'smoke': 0.0204112701, 'temp': 22.7}

    insert_data('iot_telemetry', test_data)
