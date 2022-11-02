import pymysql
from flask import Flask, jsonify

app = Flask(__name__)

conn = pymysql.connect(host='h1use0ulyws4lqr1.cbetxkdyhwsb.us-east-1.rds.amazonaws.com', user='s9cnfaowbp539mgs',
                       password='my3y3g6e934oqu2b', db='nyazi8y7vo8m9njq', charset='utf8')
# curs = conn.cursor(pymysql.cursors.DictCursor)

@app.route('/')
def hello():
    # MySQL 서버에 접속하기
    cur = conn.cursor()
    sql = "SELECT * FROM movies_221102"
    # MySQL 명령어 실행하기
    cur.execute(sql)
    # 전체 row 가져오기
    res = cur.fetchall()
    # Flask에서 제공하는 json변환 함수
    return jsonify(res)

@app.route('/search=<key>')
def search(key):
    cur = conn.cursor()
    key = key.strip()
    sql = "SELECT * FROM disney where (title like '%" + key + "%' or genre like '%" + key + "%' or original_title like '%" + key + "%')"
    cur.execute(sql)
    res = cur.fetchall()
    return jsonify(res)

if __name__ == '__main__':
    app.run()
