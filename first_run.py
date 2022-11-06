import pymysql
from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
conn = pymysql.connect(host='h1use0ulyws4lqr1.cbetxkdyhwsb.us-east-1.rds.amazonaws.com', user='s9cnfaowbp539mgs',
                       password='my3y3g6e934oqu2b', db='nyazi8y7vo8m9njq', charset='utf8')
cur = conn.cursor(pymysql.cursors.DictCursor)


@app.route('/page=<page_num>')
def hello(page_num):
    curs = conn.cursor()
    page_num = int(page_num.strip())
    res = []
    sql = "SELECT COUNT(content_id) FROM movies"
    curs.execute(sql)
    total_results = int(curs.fetchone()[0])
    if total_results % 30 == 0:
        total_pages = total_results / 30
    else:
        total_pages = int(total_results / 30) + 1

    sql = f"SELECT * FROM movies ORDER BY popularity DESC LIMIT 30 OFFSET {30 * page_num - 30}"
    cur.execute(sql)
    # 전체 row 가져오기
    data = cur.fetchall()
    jsonify(data)
    res = jsonify(
        page=page_num,
        results=data,
        total_pages=total_pages,
        total_results=total_results)
    # Flask에서 제공하는 json변환 함수
    return res


@app.route('/search=<key>/page=<page_num>')
def search(key, page_num):
    curs = conn.cursor()
    page_num = int(page_num.strip())
    res = []
    sql = "SELECT COUNT(content_id) FROM movies where (title like '%" + key + "%' or genre like '%" + key + "%' or original_title like '%" + key + "%')"
    curs.execute(sql)
    total_results = int(curs.fetchone()[0])
    if total_results % 30 == 0:
        total_pages = total_results / 30
    else:
        total_pages = int(total_results / 30) + 1

    key = key.strip()
    sql = "SELECT * FROM movies where (title like '%" + key + "%' or genre like '%" + key + "%' or original_title like '%" + key + f"%') ORDER BY popularity DESC LIMIT 30 OFFSET {30 * page_num - 30}"
    cur.execute(sql)
    data = cur.fetchall()
    jsonify(data)
    res = jsonify(
        page=page_num,
        results=data,
        total_pages=total_pages,
        total_results=total_results)
    return res


if __name__ == '__main__':
    app.run()
