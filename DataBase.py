import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DataBase:
    def __init__(self, address = 'localhost', port = '5432', login = 'postgres',
                 password = 'changeme', db_name = 'Shop', sql_file_source = 'sql_sources.sql'):
        self.address = address
        self.port = port
        self.login = login
        self.password = password
        self.db_name = db_name

        conn = psycopg2.connect('host=' + address + ' port=' + port + 'dbname=postgres' + ' user=' + login +
                                ' password=' + password)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s', (db_name, ))
        is_exists = cursor.fetchone()
        if not is_exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        conn.close()

        self.conn = psycopg2.connect('host=' + address + ' port=' + port + ' dbname=' + db_name + ' user=' + login +
                                     ' password=' + password)
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.conn.cursor()
        if not is_exists:
            with open(sql_file_source) as sql_source:
                self.cursor.execute(sql_source.read())

    def delete_database(self):
        self.conn.close()
        conn = psycopg2.connect("host=" + self.address + " port=" + self.port + " dbname=postgres" + " user=" +
                                self.login + " password=" + self.password)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(self.db_name)))
        conn.close()
        del self

    def add_detail(self, name: str, cost: int):
        if len(name) < 100:
            self.cursor.execute("SELECT * FROM add_detail(%s, %s);", (name, cost))

    def add_consumer(self, name: str, address: str):
        self.cursor.execute("SELECT add_consumer(%s, %s);", (name, address))

    def add_order(self, consumer_id: int, detail_id: int, quantity, purchase_date = None):
        if purchase_date:
            self.cursor.execute("SELECT add_order(%s, %s, %s, %s);", (consumer_id, detail_id, purchase_date, quantity))
        else:
            self.cursor.execute("SELECT add_order_default_date(%s, %s, %s);", (consumer_id, detail_id, quantity))

    def get_consumers(self):
        self.cursor.execute("SELECT * FROM get_consumers();")
        return self.cursor.fetchall()

    def get_details(self):
        self.cursor.execute("SELECT * FROM get_details();")
        return self.cursor.fetchall()

    def get_orders(self):
        self.cursor.execute("SELECT * FROM get_orders();")
        return self.cursor.fetchall()

    def clear_consumers(self):
        self.cursor.execute("SELECT clear_consumers();")

    def clear_details(self):
        self.cursor.execute("SELECT clear_details();")

    def clear_orders(self):
        self.cursor.execute("SELECT clear_orders();")

    def clear_all(self):
        self.cursor.execute("SELECT clear_all();")

    def search_orders(self, value):
        self.cursor.execute("SELECT * FROM search_orders(%s)", (value, ))
        return self.cursor.fetchall()

    def search_details(self, value):
        self.cursor.execute("SELECT * FROM search_details(%s)", (value, ))
        return self.cursor.fetchall()

    def search_consumers(self, value):
        self.cursor.execute("SELECT * FROM search_consumers(%s)", (value, ))
        return self.cursor.fetchall()

    def delete_order(self, target):
        self.cursor.execute("SELECT delete_order(%s)", (target, ))

    def delete_detail(self, target):
        self.cursor.execute("SELECT delete_detail(%s)", (target, ))

    def delete_consumer(self, target):
        self.cursor.execute("SELECT delete_consumer(%s)", (target, ))

    def update_consumer_name(self, target, value):
        if isinstance(target, int) and isinstance(value, str):
            self.cursor.execute("SELECT update_consumer_name(%s, %s)", (target, value))
        else:
            raise AttributeError("Wrong type of argument")

    def update_consumer_address(self, target, value):
        if isinstance(target, int) and isinstance(value, str):
            self.cursor.execute("SELECT update_consumer_address(%s, %s)", (target, value))
        else:
            raise AttributeError("Wrong type of argument")

    def update_detail_name(self, target, value):
        if isinstance(target, int) and isinstance(value, str):
            if len(value) < 100:
                self.cursor.execute("SELECT update_detail_name(%s, %s)", (target, value))
            else:
                raise AttributeError("Value length is greater than 100")
        else:
            raise AttributeError("Wrong type of argument")

    def update_detail_cost(self, target, value):
        if isinstance(target, int) and isinstance(value, int):
            self.cursor.execute("SELECT update_detail_cost(%s, %s)", (target, value))
        else:
            raise AttributeError("Wrong type of argument")

    def update_order_consumer_id (self, target, value):
        if isinstance(target, int) and isinstance(value, int):
            self.cursor.execute("SELECT update_order_consumer_id(%s, %s)", (target, value))
        else:
            raise AttributeError("Wrong type of argument")

    def update_order_detail_id(self, target, value):
        if isinstance(target, int) and isinstance(value, int):
            self.cursor.execute("SELECT update_order_detail_id(%s, %s)", (target, value))
        else:
            raise AttributeError("Wrong type of argument")

    def update_order_quantity(self, target, value):
        if isinstance(target, int) and isinstance(value, int):
            self.cursor.execute("SELECT update_order_quantity(%s, %s)", (target, value))
        else:
            raise AttributeError("Wrong type of argument")