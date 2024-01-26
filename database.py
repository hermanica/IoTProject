import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_card_entry(conn, card_entry):
    """
    Create a new card_entry into the cards table
    :param conn:
    :param card_entry: (card_id, entry_time)
    :return: card_entry id
    """
    sql = ''' INSERT INTO cards(card_id,entry_time,status)
              VALUES(?,?,1) '''  # 1 for inside, 0 for outside
    cur = conn.cursor()
    cur.execute(sql, card_entry)
    conn.commit()
    return cur.lastrowid

def update_card_exit(conn, card_id, exit_time):
    """
    Update the status and exit_time of a card_entry to 0 and exit_time
    :param conn:
    :param card_id: id of the card
    :param exit_time: the time of exit
    :return:
    """
    sql = ''' UPDATE cards
              SET status = 0, exit_time = ?
              WHERE card_id = ? AND status = 1 '''
    cur = conn.cursor()
    cur.execute(sql, (exit_time, card_id))
    conn.commit()


def get_cards_amount(conn):
    """
    Query all cards that are inside the parking lot
    :param conn: the Connection object
    :return: a list of cards inside
    """
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM cards WHERE status=1")
    
    data = cur.fetchone()
    if data:
        return data[0]
    return None

    

def check_card_status(conn, card_id):
    """
    Query status of a card_entry by card_id
    :param conn: the Connection object
    :param card_id:
    :return: status
    """
    cur = conn.cursor()
    cur.execute("SELECT status FROM cards WHERE card_id=? ORDER BY entry_time DESC LIMIT 1", (card_id,))

    data = cur.fetchone()
    if data:
        return data[0]  # return the status
    return None  # card not found

def get_entry_time(conn, card_id):
    
    cur = conn.cursor()
    cur.execute("SELECT entry_time FROM cards WHERE card_id=? ORDER BY entry_time DESC LIMIT 1", (card_id,))

    data = cur.fetchone()
    if data:
        return data[0]  # return the status
    return None  # card not found

def main():
    database = r"pythonsqlite.db"

    sql_create_cards_table = """ CREATE TABLE IF NOT EXISTS cards (
                                        id integer PRIMARY KEY,
                                        card_id text NOT NULL,
                                        entry_time text NOT NULL,
                                        exit_time text,
                                        status integer NOT NULL
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create cards table
        create_table(conn, sql_create_cards_table)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()

