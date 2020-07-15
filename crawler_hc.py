import pymysql
import requests
from bs4 import BeautifulSoup
conn = pymysql.connect(host='localhost', user='root', password='root', db='DBCRAW', charset='utf8')
curs = conn.cursor()
sql = """insert into tab_hc(title,contents,answer,tag)
         values (%s, %s, %s, %s)"""
ran = range(2, 10)
url = "https://hashcode.co.kr/questions/"
url_list = []
for r in ran:
    url_list.append(url + str(r))
for url in url_list:
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        title = soup.select_one('body > div.main > div.content > div.content-wrap > div.center > h2 > a')
        contents = soup.select_one(
            'body > div.main > div.content > div.content-wrap > div.center > div.content.question-body > div.markdown > p')
        answers = soup.select('div.markdown')
        for answer in answers:
            answerstring = ''.join(answer.text)
        tags = soup.select('body > div.main > div.content > div.content-wrap > div.center > div.question-tags')
        for tag in tags:
            tagstring = ''.join(tag.text)
        curs.execute(sql, (title.text, contents.text, answerstring, ''.join(tagstring.splitlines())))
    except:
        print('error')
conn.commit()
conn.close()