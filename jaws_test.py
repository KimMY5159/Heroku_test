import json
import urllib.request
import ssl
import time
import pandas
import pymysql
from sqlalchemy import create_engine

# conn = pymysql.connect(host='localhost', user='root', password='111111', db='capstone_db', charset='utf8')
engine = 'mysql+pymysql://s9cnfaowbp539mgs:'+'my3y3g6e934oqu2b'+'@h1use0ulyws4lqr1.cbetxkdyhwsb.us-east-1.rds.amazonaws.com/nyazi8y7vo8m9njq'
# curs = conn.cursor(pymysql.cursors.DictCursor)
db = create_engine(engine, encoding='utf-8')
conn = db.connect()

start = time.time()
today = time.strftime('%y%m%d')


def genre_select(genre_key):
    val = {28: "액션", 12: "모험", 16: "애니메이션", 35: "코미디",
           80: "범죄", 99: "다큐멘터리", 18: "드라마",
           10751: "가족", 14: "판타지", 36: "역사", 27: "공포",
           10402: "음악", 9648: "미스터리", 10749: "로맨스",
           878: "SF", 10770: "TV 영화", 53: "스릴러",
           10752: "전쟁", 37: "서부"}.get(genre_key, "null")
    return val


# urlretrieve 권한
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)
ssl._create_default_https_context = ssl._create_unverified_context

#ott_id = ['8', '337', '356', '97']
#ott_name = ['Netflix', 'DisneyPlus', 'wavve', 'Watcha']
ott_id = ['337']
ott_name = ['DisneyPlus']
nametmp = 0

content_id = []
platform = []
original_title = []
title = []
genre = []
overview = []
popularity = []
vote_average = []
vote_count = []
release_date = []
original_language = []
poster_path = []
back_path = []
detail_path = []

for ottid in ott_id:
    url = f'https://api.themoviedb.org/3/discover/movie?api_key=e8f7349fccfcd372e14b13ff4c69840f&with_watch_providers={ottid}&watch_region=KR&language=ko&page='
    image_url = "https://image.tmdb.org/t/p/w500"
    text_data = urllib.request.urlopen(url).read().decode('utf-8')
    bring_max_page = json.loads(text_data)
    max_page = bring_max_page['total_pages']
    if max_page > 350:
        max_page = 350

    print(f'{ott_name[nametmp]} 영화 목록 가져오기 시작')

    for i in range(1, max_page + 1):
        print(f'현재 페이지 : {i}')
        page_url = url + str(i)
        text_data = urllib.request.urlopen(page_url).read().decode('utf-8')
        movies = json.loads(text_data)
        for j in range(0, len(movies['results'])):
            data = movies['results'][j]
            print(data['title'])
            if data['id'] in content_id:
                platform[content_id.index(data['id'])] += ', ' + ott_name[nametmp]
                continue
            content_id.append(data['id'])
            platform.append(ott_name[nametmp])
            original_title.append(data['original_title'])
            title.append(data['title'])
            overview.append(data['overview'])
            popularity.append(data['popularity'])
            vote_average.append(data['vote_average'])
            vote_count.append(data['vote_count'])
            original_language.append(data['original_language'])
            detail_path.append(f'https://api.themoviedb.org/3/movie/{data["id"]}?api_key'
                               f'=e8f7349fccfcd372e14b13ff4c69840f&language=ko')
            if 'release_date' in data:
                release_date.append(data['release_date'])
            else:
                release_date.append('')
            temp = ''
            for k in range(0, len(data['genre_ids'])):
                temp = temp + genre_select(data['genre_ids'][k]) + ', '
            temp = temp[:-2]  # 마지막 쉼표와 공백삭제
            genre.append(temp)
            if data['poster_path'] is None:
                poster_path.append('')
            else:
                poster_path.append(image_url + data['poster_path'])
            if data['backdrop_path'] is None:
                back_path.append('')
            else:
                back_path.append(image_url + data['backdrop_path'])
    nametmp += 1

print('영화 목록 csv파일 작성 시작')

df = pandas.DataFrame()
df['content_id'] = content_id
df['platform'] = platform
df['original_title'] = original_title
df['title'] = title
df['genre'] = genre
df['overview'] = overview
df['popularity'] = popularity
df['vote_average'] = vote_average
df['vote_count'] = vote_count
df['release_date'] = release_date
df['original_language'] = original_language
df['poster_path'] = poster_path
df['back_path'] = back_path
df['detail_path'] = detail_path
# df.to_csv(f'movies_{today}.csv', index=False, encoding='utf-8')

print('실행시간 : ', time.time() - start)

df.to_sql(name=f'movies_{today}', con=db, if_exists='append',index=False)
conn.close()