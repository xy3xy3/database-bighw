from database import db

class KnowledgeBaseModel:
    def __init__(self):
        self.conn = db.get_connection()
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        db.release_connection(self.conn)

    def create(self, name, desc, model_id):
        query = """
        INSERT INTO knowledgebase (name, desc, model_id)
        VALUES (%s, %s, %s)
        RETURNING id;
        """
        self.cursor.execute(query, (name, desc, model_id))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def get_by_id(self, id):
        query = """
        SELECT * FROM knowledgebase WHERE id = %s;
        """
        self.cursor.execute(query, (id,))
        return self.cursor.fetchone()

    def get_all(self):
        query = """
        SELECT * FROM knowledgebase;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update(self, id, name, desc, model_id):
        query = """
        UPDATE knowledgebase
        SET name = %s, desc = %s, model_id = %s
        WHERE id = %s;
        """
        self.cursor.execute(query, (name, desc, model_id, id))
        self.conn.commit()

    def delete(self, id):
        query = """
        DELETE FROM knowledgebase WHERE id = %s;
        """
        self.cursor.execute(query, (id,))
        self.conn.commit()