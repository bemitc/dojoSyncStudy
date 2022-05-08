#!/usr/bin/env python3

from flask import Flask, request, Response
import sys
import os
import sqlite3

app = Flask(__name__)

STUDY_DB_PATH = os.environ.get("STUDY_DB_PATH")
db_conn = sqlite3.connect(STUDY_DB_PATH)


@app.route('/api/pgn/<studyId>/<chapterId>.pgn', methods=['GET'])
def getPgn(studyId, chapterId):
    studyChapterId = str(studyId) + str(chapterId)
    db_conn = sqlite3.connect(os.environ.get("STUDY_DB_PATH"))
    db_cursor = db_conn.cursor()

    db_cursor.execute('''SELECT pgn FROM Studies WHERE StudyChapterId=?''', (str(studyChapterId),))
    rows = db_cursor.fetchall()
    for r in rows:
        resp = Response(str(r[0]), mimetype='application/x-chess-pgn')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return ""
    db_conn.close()

