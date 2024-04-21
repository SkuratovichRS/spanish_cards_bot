import psycopg2
import random


class WordsDatabase:

    def __init__(self, name, user, password):
        self.name = name
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        self.remaining_main_words = {}
        self.remaining_user_words = {}
        self.cycle = True

    def connect(self) -> None:
        self.connection = (psycopg2.connect(
            database=self.name, user=self.user, password=self.password))
        self.cursor = self.connection.cursor()

    def disconnect(self) -> None:
        self.connection.commit()
        self.connection.close()

    def create_tables(self) -> None:
        self.connect()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS main_words(
            id SERIAL PRIMARY KEY,
            word VARCHAR(40) NOT NULL,
            translate VARCHAR(40) NOT NULL);
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS main_words_variants(
            word_id INT NOT NULL,
            variant VARCHAR(40) NOT NULL,
            FOREIGN KEY(word_id) REFERENCES main_words(id));
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users_words(
            id SERIAL PRIMARY KEY,
            word VARCHAR(40) NOT NULL,
            translate VARCHAR(40) NOT NULL,
            chat_id BIGINT NOT NULL);
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users_words_variants(
            word_id INT NOT NULL,
            variant VARCHAR(40) NOT NULL,
            FOREIGN KEY(word_id) REFERENCES users_words(id));
        """)
        self.disconnect()

    def fill_table_main_words(self, word: str, translate: str) -> None:
        self.connect()
        self.cursor.execute("""
            INSERT INTO main_words (word, translate)
            VALUES (%s, %s);
            """, (word, translate))
        self.disconnect()

    def fill_table_main_words_variants(
            self, word_id: int, translations: list) -> None:
        self.connect()
        for translate in translations:
            self.cursor.execute("""
                INSERT INTO main_words_variants (word_id, variant)
                VALUES (%s, %s);
                """, (word_id, translate))
        self.disconnect()

    def fill_table_users_words(
            self,
            word: str,
            translate: str,
            chat_id: int) -> None:
        self.connect()
        self.cursor.execute("""
            INSERT INTO users_words (word, translate, chat_id)
            VALUES (%s, %s, %s);
            """, (word, translate, chat_id))
        self.disconnect()

    def get_user_word_id(self, word: str, chat_id: int) -> int:
        self.connect()
        self.cursor.execute("""
            SELECT id FROM users_words
            WHERE word=%s and chat_id=%s;
            """, (word, chat_id))
        word_id = self.cursor.fetchone()[0]
        return word_id

    def fill_table_users_words_variants(
            self, word_id: int, translations: list) -> None:
        self.connect()
        for translate in translations:
            self.cursor.execute("""
                INSERT INTO users_words_variants (word_id, variant)
                VALUES (%s, %s);
                """, (word_id, translate))
        self.disconnect()

    def get_all_words(self, chat_id: int) -> list:
        self.connect()
        self.cursor.execute('SELECT word FROM main_words')
        all_words = [row[0] for row in self.cursor.fetchall()]
        self.cursor.execute(
            'SELECT word FROM users_words WHERE chat_id=%s', (chat_id,))
        all_words += [row[0] for row in self.cursor.fetchall()]
        self.disconnect()
        return all_words

    def get_user_words(self, chat_id: int) -> list:
        self.connect()
        self.cursor.execute(
            'SELECT word FROM users_words WHERE chat_id=%s', (chat_id,))
        user_words = [row[0] for row in self.cursor.fetchall()]
        self.disconnect()
        return user_words

    def get_remaining_words(self, chat_id: int) -> None:
        self.connect()
        self.cursor.execute('SELECT word FROM main_words')
        self.remaining_main_words[chat_id] = [row[0]
                                              for row in self.cursor.fetchall()]
        self.cursor.execute(
            'SELECT word FROM users_words WHERE chat_id=%s', (chat_id,))
        self.remaining_user_words[chat_id] = [row[0]
                                              for row in self.cursor.fetchall()]
        self.disconnect()

    def get_random_word(self, chat_id) -> tuple | None:
        if len(
                self.remaining_main_words[chat_id] +
                self.remaining_user_words[chat_id]) == 1:
            self.cycle = False
        if self.remaining_main_words[chat_id] or self.remaining_user_words[chat_id]:
            random_word = random.choice(self.remaining_main_words[chat_id]
                                        + self.remaining_user_words[chat_id])
            if random_word in self.remaining_main_words[chat_id]:
                self.remaining_main_words[chat_id].remove(random_word)
                self.connect()
                self.cursor.execute(
                    "SELECT * FROM main_words WHERE word=%s", (random_word,))
                row = self.cursor.fetchone()
                self.cursor.execute(
                    "SELECT * FROM main_words_variants WHERE word_id=%s", (row[0],))
                fetched = self.cursor.fetchall()
                translations = [f[1] for f in fetched]
                self.disconnect()
                return row[1:], translations
            else:
                self.remaining_user_words[chat_id].remove(random_word)
                self.connect()
                self.cursor.execute(
                    "SELECT * FROM users_words WHERE word=%s", (random_word,))
                row = self.cursor.fetchone()
                self.cursor.execute(
                    "SELECT * FROM users_words_variants WHERE word_id=%s", (row[0],))
                fetched = self.cursor.fetchall()
                translations = [f[1] for f in fetched]
                self.disconnect()
                return row[1:], translations
        else:
            return None, None

    def delete_user_word(self, word: str, chat_id: int) -> None:
        word_id = self.get_user_word_id(word, chat_id)
        self.connect()
        self.cursor.execute("""
            DELETE FROM users_words_variants WHERE word_id=%s
            """, (word_id,))
        self.cursor.execute("""
            DELETE FROM users_words WHERE word=%s and chat_id=%s
            """, (word, chat_id))
        self.disconnect()
