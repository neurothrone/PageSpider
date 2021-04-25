import sqlite3 as db


def create_database(database_path: str):
    # If no database exists; create one, otherwise connect
    conn = db.connect(database_path)
    with conn:
        cur = conn.cursor()
        cur.execute("drop table if exists words")

        ddl = r"""
        create table words
        (
            word TEXT not null
                constraint words_pk
                    primary key,
            usage_count int default 1 not null
        );"""
        cur.execute(ddl)

        ddl = r"""
        create unique index words_word_uindex
            on words (word);"""
        cur.execute(ddl)


def save_words_to_database(database_path: str, words_list: list):
    conn = db.connect(database_path)
    with conn:
        cur = conn.cursor()
        for word in words_list:
            sql = "select count(word) from words where word='" + word + "'"
            cur.execute(sql)
            count = cur.fetchone()[0]
            if count > 0:
                sql = "update words set usage_count = usage_count + 1 where word = '" + word + "'"
            else:
                sql = "insert into words(word) values ('" + word + "')"
            cur.execute(sql)

    print("Database completed saving words.")
