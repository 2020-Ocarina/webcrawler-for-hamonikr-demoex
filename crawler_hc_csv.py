import requests
import pandas as pd
from bs4 import BeautifulSoup

# url 뒤에 붙을 숫자 범위
ran = range(10038, 11038)
url = "https://hashcode.co.kr/questions/"
# url 뒤에 지정한 범위 내의 숫자를 붙여 배열에 저장
url_list = []

for r in ran:
    url_list.append(url + str(r))
movie_review = []
for url in url_list:
    print(url)
    # 파싱 작업
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    #제목 추출
    title = soup.select('body > div.main > div.content > div.content-wrap > div.center > h2 > a')

    #본문 추출
    contents = soup.select(
        'body > div.main > div.content > div.content-wrap > div.center > div.content.question-body > div.markdown')

    #답변 추출
    answers = soup.select(
        'div.answer-wrap > ul.answers-list > li > div.center > div.markdown')
    # 답변은 여러개일 수 있어 배열 형태이기 때문에 이를 모두 합쳐준다
    list=[]
    for answer in answers:
        list.append(answer.text)

    #답변들을 구분해줄 문자열(<------->)을 사이에 추가한다.
    answer_str="\n\n<-------------------------------->\n\n".join(list)

    # 태그 추출
    tag = soup.select(
        'body > div.main > div.content > div.content-wrap > div.center > div.question-tags')

    for item in zip(title, contents, answer_str, tag):
        movie_review.append(
            {
                '제목': item[0].text,
                '내용': item[1].text,
                '답변': answer_str,
                '태그': item[3].text.replace('\n', '').replace('\t', '').replace('  ', '')
            }
        )

data = pd.DataFrame(movie_review)
data.to_csv('finaltest.csv')
