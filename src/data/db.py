import asyncio
import aiosqlite


class DBCommands:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    async def connect(self):
        self.connection = await aiosqlite.connect(self.db_path)
        await self.create_table()

    async def close(self):
        if self.connection is not None:
            await self.connection.close()

    async def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS word (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_in_original_lang TEXT NOT NULL,
            word_translation TEXT NOT NULL,
            weight INTEGER
        )
        '''
        await self.connection.execute(query)
        await self.connection.commit()

    async def add_word(self, word, translation, weight=5):
        await self.connection.execute("INSERT INTO word (word, translation, weight) VALUES (?, ?, ?)",
                                      (word, translation, weight))
        await self.connection.commit()

    async def get_random_word(self):
        cursor = await self.connection.execute("SELECT word, translation, weight FROM word ORDER BY RANDOM() LIMIT 6")
        words = await cursor.fetchall()
        return words

    async def check_if_word_exists(self, word: str) -> bool:
        cursor = await self.connection.execute("SELECT * FROM word WHERE word = ?",
                                               (word, ))
        words = await cursor.fetchall()
        return bool(len(words))

    async def increase_weight(self, word: str):
        await self.connection.execute("UPDATE word SET weight = weight + 5 "
                                      "WHERE word = ? OR translation = ?", (word, word))
        await self.connection.commit()

    async def decrease_weight(self, word: str):
        assert isinstance(word, str) is True
        await self.connection.execute("UPDATE word SET weight = MAX(weight - 1, 1) "
                                      "WHERE word = ? OR translation = ?", (word, word))
        await self.connection.commit()
