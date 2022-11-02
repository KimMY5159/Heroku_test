import pymysql
from flask import Flask, jsonify

app = Flask(__name__)

conn = pymysql.connect(host='us-cdbr-east-06.cleardb.net', user = 'bb0a771f38c75f', password='9921acd2', db = 'heroku_ca',charset = 'utf8')
# curs = conn.cursor(pymysql.cursors.DictCursor)

@app.route('/')
def hello():
    # MySQL 서버에 접속하기
    cur = conn.cursor()
    sql = "SELECT * FROM movies_221103"
    # MySQL 명령어 실행하기
    cur.execute(sql)
    # 전체 row 가져오기
    res = cur.fetchall()
    # Flask에서 제공하는 json변환 함수
    return jsonify(res)

@app.route('/search?keywords=<key>')
def search(key):
    sql = "SELECT * FROM movies_221103 where title or genre like '%"+key+"'%'"
    cur.execute(sql)
    res = cur.fetchall()
    return jsonify(res)

if __name__ == '__main__':
    app.run()
