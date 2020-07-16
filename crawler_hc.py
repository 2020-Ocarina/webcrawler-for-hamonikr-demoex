import pymysql
import requests
from bs4 import BeautifulSoup

# db와 연결
conn = pymysql.connect(host='localhost', user='root', password='root', db='DBCRAW', charset='utf8')
curs = conn.cursor()

# mysql 실행 명령문
sql = """insert into tab_hc(title,contents,answer,tag)
         values (%s, %s, %s, %s)"""

ran = range(4, 10)  # url 뒤에 붙을 숫자 범위
url = "https://hashcode.co.kr/questions/"
url_list = []

# url 뒤에 지정한 범위 내의 숫자를 붙여 배열에 저장
for r in ran:
    url_list.append(url + str(r))

for url in url_list:
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')  # 파싱 작업
        # 제목 추출
        title = soup.select_one('body > div.main > div.content > div.content-wrap > div.center > h2 > a')
        # 내용 추출
        contents = soup.select_one(
            'body > div.main > div.content > div.content-wrap > div.center > div.content.question-body > div.markdown > p')
        # 답변 추출
        answers = soup.select('div.markdown')
        # 답변은 여러개일 수 있어 배열 형태이기 때문에 이를 모두 합쳐준다
        for answer in answers:
            answerstring = ''.join(answer.text)
        # 태그 추출
        tags = soup.select('body > div.main > div.content > div.content-wrap > div.center > div.question-tags')
        # 태그는 여러개일 수 있어 배열 형태이기 때문에 이를 모두 합쳐준다
        for tag in tags:
            tagstring = ''.join(tag.text)
        # db에 저장. 태그들 사이의 엔터는 없앤다.
        curs.execute(sql, (title.text, contents.text, answerstring, ''.join(tagstring.splitlines())))
    # 삭제된 글일 경우 에러 출력하고 다음 진행
    except:
        print('error')
conn.commit()
conn.close()