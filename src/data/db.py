import asyncio
import aiosqlite
from async_lru import alru_cache


#
# class DBCommands:
#     def __new__(cls, *args, **kwargs):
#         if not hasattr(cls, '_instance'):
#             cls._instance = super(DBCommands, cls).__new__(cls)
#         return cls._instance
#
#     def __init__(self, db_path):
#         self.db_name = db_path
#         self.connection = None
#
#     async def connect(self):
#         self.connection = await aiosqlite.connect(self.db_name)
#         await self.create_table()
#
#     async def close(self):
#         if self.connection is not None:
#             await self.connection.close()
#
#     async def create_table(self):
#         query = '''
#         CREATE TABLE IF NOT EXISTS word (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             word_in_original_lang TEXT NOT NULL,
#             word_translation TEXT NOT NULL,
#             weight INTEGER
#         )
#         '''
#         await self.connection.execute(query)
#         await self.connection.commit()
#
#     async def add_new_word(self, word: str, translate: str, weight=5) -> None:
#         """New word add process"""
#         query = 'INSERT INTO word (word_in_original_lang, word_translation, weight) VALUES (?, ?, ?)'
#         await self.connection.execute(query, (word, translate, weight))
#         await self.connection.commit()
#
#     @alru_cache
#     async def get_all_words(self) -> dict[str, str]:
#         query = 'SELECT word_in_original_lang, word_translation, weight FROM word'
#         cursor = await self.connection.execute(query)
#         rows = await cursor.fetchall()
#         print(rows)
#         await cursor.close()
#         return rows
#
#     async def increase_weight(self, word):
#         query = "UPDATE word SET weight = weight + 1 WHERE word = ?"
#         self.connection.execute(query, (word,))
#         self.connection.commit()
#
#     async def reset_weights(self):
#         self.connection.execute("UPDATE words SET weight = 1")
#         self.connection.commit()


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

    async def increase_weight(self, word: str):
        await self.connection.execute("UPDATE word SET weight = weight + 5 "
                                      "WHERE word = ? OR translation = ?", (word, word))
        await self.connection.commit()

    async def decrease_weight(self, word: str):
        assert isinstance(word, str) is True
        await self.connection.execute("UPDATE word SET weight = MAX(weight - 1, 1) "
                                      "WHERE word = ? OR translation = ?", (word, word))
        await self.connection.commit()


async def main():
    vocab = DBCommands('./words.db')
    await vocab.connect()
    await vocab.create_table()
    while True:
        random_word = await vocab.get_random_word()
        print(random_word)
        break

    await vocab.close()


if __name__ == '__main__':
    asyncio.run(main())
