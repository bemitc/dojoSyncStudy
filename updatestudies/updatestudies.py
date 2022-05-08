#!/usr/bin/env python3

import lichess.api
import os
from dotenv import *
from lichess.format import PGN
import sqlite3
import sys
import io
import chess.pgn

def load_settings():
    load_dotenv(find_dotenv())

def ExportStudy(studyId, auth):
    api = lichess.api.DefaultApiClient()

    try:
        res=api.call("/api/study/{}.pgn".format(studyId), auth=LICHESS_AUTH, format=lichess.format.PGN, object_type=lichess.format.GAME_OBJECT)
    except:
        return None
    else:
        return res

def create_database(dbfile):
    conn = sqlite3.connect(dbfile)

    if conn != None:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Studies
                     (StudyChapterId TEXT NOT NULL PRIMARY KEY, pgn TEXT NOT NULL);''')
        conn.commit()

    return conn

# load settings
load_settings()
LICHESS_AUTH = os.environ.get("LICHESS_AUTH")
STUDY_DB_PATH = os.environ.get("STUDY_DB_PATH")

db_conn = create_database(STUDY_DB_PATH)
db_cursor = db_conn.cursor()

for arg in sys.argv[1:]:
    study = ExportStudy(arg, LICHESS_AUTH)

    if study == None:
        continue

    pgn = io.StringIO(study)

    while True:
        game = chess.pgn.read_game(pgn)
        gameText = str(game) + "\n\n"
        if game == None:
            break

        if len(game.headers["Site"]) == 43 and game.headers["Site"][0:26] == "https://lichess.org/study/":
            studychapter = game.headers["Site"][26:].split('/')
            db_cursor.execute('''INSERT INTO Studies (StudyChapterId, pgn)
                                 VALUES (?, ?) ON CONFLICT (StudyChapterId) DO UPDATE SET pgn=excluded.pgn;''', (str(studychapter[0]+studychapter[1]), str(gameText)))
db_conn.commit()
db_conn.close()

