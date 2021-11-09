import unittest
import testing.postgresql
import psycopg2
# from sqlalchemy import create_engine, engine


class TestDB(unittest.TestCase):
    def setUp(self):
        self.postgresql = testing.postgresql.Postgresql()

    def tearDown(self):
        self.postgresql.stop()

    def test_create_table(self):
        table_query = '''CREATE TABLE users(
    username CHAR(30) NOT NULL,
    firstname CHAR(50),
    lastname CHAR(50),
    password CHAR(50) NOT NULL
);'''
        insert_query = '''INSERT INTO users (username, firstname, lastname, password)
VALUES ("pinheadlarry", "Patrick", "Starr", "SpongebobBFF");'''

        select_query = '''SELECT * FROM users;'''

        conn = psycopg2.connect(**self.postgresql.dsn())
        cursor = conn.cusor()
        cursor.execute(table_query)
        cursor.execute(insert_query)
        query = cursor.execute(select_query)
        
        
        self.assertEqual(query, print(query))
        

if __name__ == '__main__':
    unittest.main()