import json
import pathlib
import sqlite3

class BlockHashesAdapter:
    """
    Base class to build adapters to store files hashes for versioning.

    Translated files use hashes from their origin file to control which
    Markdown blocks were already translated.
    """
    def __init__(self, folder="."):
        pass
        
    def set(self, file_name, hashes):
        return None

    def get(self, file_name):
        return None

    def delete(self, file_name):
        return None

class BlockHashesJSONAdapter(BlockHashesAdapter):
    def __init__(self, folder="."):
        self.filename = pathlib.Path(folder) / f"hashes.json"
        if self.filename.exists():
            self.data = json.loads(self.filename.read_text(encoding="utf-8"))
        else:
            self.data = {}

    def set(self, file_name, hashes):
        self.data[str(file_name)] = hashes
        self._save()

    def get(self, file_name):
        return self.data.get(str(file_name), None)

    def delete(self, file_name):
        file_name = str(file_name)
        if file_name in self.data:
            del self.data[file_name]
            self._save()

    def _save(self):
        with self.filename.open('w', encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)

class BlockHashesSQLAdapter(BlockHashesAdapter):
    def __init__(self, folder="."):
        self.dbname = pathlib.Path(folder) / "hashes.db"
        self.conn = sqlite3.connect(str(self.dbname))
        self._initialize_db()

    def _initialize_db(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS hashes (
                    file_name TEXT PRIMARY KEY,
                    hash_values TEXT
                )
            """)

    def set(self, file_name, hashes):
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO hashes (file_name, hash_values)
                VALUES (?, ?)
            """, (str(file_name), json.dumps(hashes)))

    def get(self, file_name):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT hash_values FROM hashes WHERE file_name = ?
        """, (str(file_name),))
        result = cursor.fetchone()
        return json.loads(result[0]) if result else None

    def delete(self, file_name):
        with self.conn:
            self.conn.execute("""
                DELETE FROM hashes WHERE file_name = ?
            """, (str(file_name),))
