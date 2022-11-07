import pymysql
from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
conn = pymysql.connect(host='h1use0ulyws4lqr1.cbetxkdyhwsb.us-east-1.rds.amazonaws.com', user='s9cnfaowbp539mgs',
                       password='my3y3g6e934oqu2b', db='nyazi8y7vo8m9njq', charset='utf8')
cur = conn.cursor(pymysql.cursors.DictCursor)

# curs = conn.cursor(pymysql.cursors.DictCursor)


@app.route('/')
def hello():
    return '''
    <!DOCTYPE HTML><html>
    <head><h1>api사용법</h1></head>
    <body>
    <pre>
        <br>
        기본 경로(필수) :     kmy-heroku-test.herokuapp.com<br>
        (필수)              /contents={movies, tv, webtoon, webnovel}<br>
        (선택:플랫폼)        /platform={movies&tv=[Netflix,DisneyPlus,wavve,Watcha],webtoon&webnovel=[naver,kakopage]}
        (선택:검색)          /search={검색어}<br>
        (필수)              /page={페이지숫자}
        
        컨텐츠는 한 페이지에 최대30개씩 표시됩니다.
        영화와 tv시리즈 검색은 원제,번역제목,장르 검색 가능합니다.
        정렬은 기본적으로 영화와 tv시리즈는 컨텐츠의 인기도 내림차순, 웹툰과 웹소설은 작품의 평균평점 내림차순으로 정렬됩니다.
        웹툰과 웹소설 검색은 제목,장르,작가 검색이 가능합니다. 혹은 'X요일'과 같은 식으로 특정요일 연재작품 검색이 가능합니다.
    </pre>
    </body>
    '''


@app.route('/contents=<content>/page=<page_num>')
def all_contents(content, page_num):
    if content == 'movies' or content == 'tv':
        sort_by = 'popularity'
        ident = 'content_id'
    elif content == 'webtoon' or content == 'webnovel':
        sort_by = 'rating'
        ident = 'id_list'

    curs = conn.cursor()
    page_num = int(page_num.strip())
    res = []
    sql = f"SELECT COUNT({ident}) FROM {content}"
    curs.execute(sql)
    total_results = int(curs.fetchone()[0])
    if total_results % 30 == 0:
        total_pages = total_results / 30
    else:
        total_pages = int(total_results / 30) + 1

    sql = f"SELECT * FROM {content} ORDER BY {sort_by} DESC LIMIT 30 OFFSET {30 * page_num - 30}"
    cur.execute(sql)
    # 전체 row 가져오기
    data = cur.fetchall()
    jsonify(data)
    res = jsonify(
        page=page_num,
        results=data,
        total_pages=total_pages,
        total_results=total_results)
    return res


@app.route('/contents=<content>/platform=<platform>/page=<page_num>')
def contents_with_platform(content, platform, page_num):
    if content == 'movies' or content == 'tv':
        sort_by = 'popularity'
        ident = 'content_id'
    elif content == 'webtoon' or content == 'webnovel':
        sort_by = 'rating'
        ident = 'id_list'

    curs = conn.cursor()
    page_num = int(page_num.strip())
    res = []
    sql = f"SELECT COUNT({ident}) FROM {content} where platform like '%{platform}%'"
    curs.execute(sql)
    total_results = int(curs.fetchone()[0])
    if total_results % 30 == 0:
        total_pages = total_results / 30
    else:
        total_pages = int(total_results / 30) + 1

    sql = f"SELECT * FROM {content} where platform like '%{platform}%' ORDER BY {sort_by} DESC LIMIT 30 OFFSET {30 * page_num - 30}"
    cur.execute(sql)
    # 전체 row 가져오기
    data = cur.fetchall()
    jsonify(data)
    res = jsonify(
        page=page_num,
        results=data,
        total_pages=total_pages,
        total_results=total_results)
    return res


@app.route('/contents=<content>/search=<key>/page=<page_num>')
def search(content, key, page_num):
    if content == 'movies' or content == 'tv':
        sort_by = 'popularity'
        ident = 'content_id'
        where = f"(title like '%{key}%' or genre like '%{key}%' or original_title like '%{key}%')"
    elif content == 'webtoon' or content == 'webnovel':
        sort_by = 'rating'
        ident = 'id_list'
        if '요' in key:
          where = "day like '%{key[:1]}%'"
        else:
          where = f"(title like '%{key}%' or genre like '%{key}%' or author like '%{key}%')"

    curs = conn.cursor()
    page_num = int(page_num.strip())
    res = []
    sql = f"SELECT COUNT({ident}) FROM {content} where {where}"
    curs.execute(sql)
    total_results = int(curs.fetchone()[0])
    if total_results % 30 == 0:
        total_pages = total_results / 30
    else:
        total_pages = int(total_results / 30) + 1

    key = key.strip()
    sql = f"SELECT * FROM {content} where {where} ORDER BY {sort_by} DESC LIMIT 30 OFFSET {30 * page_num - 30}"
    cur.execute(sql)
    data = cur.fetchall()
    jsonify(data)
    res = jsonify(
        page=page_num,
        results=data,
        total_pages=total_pages,
        total_results=total_results)
    return res


@app.route('/contents=<content>/platform=<platform>/search=<key>/page=<page_num>')
def search_with_platform(content, platform, key, page_num):
    if content == 'movies' or content == 'tv':
        sort_by = 'popularity'
        ident = 'content_id'
        where = f"(title like '%{key}%' or genre like '%{key}%' or original_title like '%{key}%')"
    elif content == 'webtoon' or content == 'webnovel':
        sort_by = 'rating'
        ident = 'id_list'
        if '요일' in key:
          where = "day like '%{key[:1]}%'"
        else:
          where = f"(title like '%{key}%' or genre like '%{key}%' or author like '%{key}%')"

    curs = conn.cursor()
    page_num = int(page_num.strip())
    res = []
    sql = f"SELECT COUNT({ident}) FROM {content} where (platform like '%{platform}%' and {where})"
    curs.execute(sql)
    total_results = int(curs.fetchone()[0])
    if total_results % 30 == 0:
        total_pages = total_results / 30
    else:
        total_pages = int(total_results / 30) + 1

    key = key.strip()
    sql = f"SELECT * FROM {content} where (platform like '%{platform}%' and {where}) ORDER BY {sort_by} DESC LIMIT 30 OFFSET {30 * page_num - 30}"
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
