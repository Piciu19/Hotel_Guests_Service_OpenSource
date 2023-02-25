import psycopg2
class PostgressConnection:

    def __init__(self, host, db, username, pwd, port):
        self.host = host
        self.db = db
        self.username = username
        self.pwd = pwd
        self.port = port

    def __del__(self):
        del self.host
        del self.db
        del self.username
        del self.pwd
        del self.port

    def schemaTable(self, schemaScript, tableScript):
        try:
            conn = psycopg2.connect(
                host=self.host,
                dbname=self.db,
                user=self.username,
                password=self.pwd,
                port=self.port)

            cur = conn.cursor()

            if schemaScript != None:
                cur.execute(schemaScript)
                conn.commit()
            if schemaScript != None:
                cur.execute(tableScript)
                conn.commit()

        except Exception as error:
            print(error)
        finally:
            cur.close()
            conn.close()

    def add(self, executeScript, executeValues):
        try:
            conn = psycopg2.connect(
                host=self.host,
                dbname=self.db,
                user=self.username,
                password=self.pwd,
                port=self.port)

            cur = conn.cursor()

            if executeScript != None:
                cur.execute(executeScript, executeValues)
                conn.commit()
        except Exception as error:
            print(error)
        finally:
            cur.close()
            conn.close()
    def view(self, executeScript):
        try:
            conn = psycopg2.connect(
                host=self.host,
                dbname=self.db,
                user=self.username,
                password=self.pwd,
                port=self.port)

            cur = conn.cursor()

            if executeScript != None:
                cur.execute(executeScript)
                for record in cur.fetchall():
                    print(record[0], record[1], record[2], record[3], record[4], record[5])

        except Exception as error:
            print(error)
        finally:
            cur.close()
            conn.close()

    def delete(self,executeScript, executeValues):
        try:
            conn = psycopg2.connect(
                host=self.host,
                dbname=self.db,
                user=self.username,
                password=self.pwd,
                port=self.port)

            cur = conn.cursor()

            if executeScript != None:
                cur.execute(executeScript, executeValues)
                conn.commit()
        except Exception as error:
            print(error)
        finally:
            cur.close()
            conn.close()