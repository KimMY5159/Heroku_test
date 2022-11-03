import pymysql
from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
conn = pymysql.connect(host='h1use0ulyws4lqr1.cbetxkdyhwsb.us-east-1.rds.amazonaws.com', user='s9cnfaowbp539mgs',
                       password='my3y3g6e934oqu2b', db='nyazi8y7vo8m9njq', charset='utf8')
cur = conn.cursor(pymysql.cursors.DictCursor)

@app.route('/page=<page_num>')
def hello(page_num):
    page_num = int(page_num.strip())
    # MySQL 서버에 접속하기
    sql = f"SELECT * FROM movies_221102 ORDER BY popularity DESC ORDERS LIMIT 30 OFFSET {30*page_num-29}"
    # MySQL 명령어 실행하기
    cur.execute(sql)
    # 전체 row 가져오기
    res = cur.fetchall()
    # Flask에서 제공하는 json변환 함수
    return jsonify(res)

@app.route('/search=<key>')
def search(key):
    key = key.strip()
    sql = "SELECT * FROM movies_221102 where (title like '%" + key + "%' or genre like '%" + key + "%' or original_title like '%" + key + "%')"
    cur.execute(sql)
    res = cur.fetchall()
    return jsonify(res)

if __name__ == '__main__':
    app.run()
