# coding = UTF8

import os
import random
import sqlite3

DB_NAME = "db/restaurant.db"
TABLE_NAME = "restaurant"

INSERT_SQL = """
INSERT INTO restaurant(name)
VALUES('{}');
"""

def install():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{}';".format(TABLE_NAME))
    if not cur.fetchall():
        conn.executescript("CREATE TABLE restaurant(name varchar(100) NOT NULL);")

def uninstall():
    os.remove(DB_NAME)

def add_restaurant(name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.executescript(INSERT_SQL.format(name))
    conn.commit()
    conn.close()

def choose():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    rows = conn.execute("SELECT name FROM restaurant;").fetchall()
    assert len(rows) != 0

    random.shuffle(rows)
    # for row in :
    #     result.append(row[0])
    return rows[0][0]


