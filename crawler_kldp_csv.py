import requests
import pandas as pd
from bs4 import BeautifulSoup

# url 뒤에 붙을 숫자 범위
ran = range(1, 163620)
url = "https://kldp.org/node/"

# url 뒤에 지정한 범위 내의 숫자를 붙여 배열에 저장
url_list = []
for r in ran:
    url_list.append(url + str(r))

data_list = []  # 전체 데이터 저장하는 리스트

title_num = 1   # 글번호 저장하는 변수

for url in url_list:

    # 진행 상황 파악하기 위해 링크 출력
    print(url)
    # 파싱 작업
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    #제목 추출
    title = soup.select('#page-title')
    #본문 추출
    contents = soup.select(
        'div.content > div.field.field-name-body.field-type-text-with-summary.field-label-hidden > div')
    #답변 추출
    answers = soup.select('div.comment')
    #태그 추출
    tags = soup.select('div.content > div.field.field-name-taxonomy-forums.field-type-taxonomy-term-reference.field-label-above > div.field-items > div > a')
    if not tags:
        tag_str="No tags Exist"
    if tags:
        tag_str=tags[0].text
    # 답변이 존재하지 않을 경우 예외 처리
    if not answers:
        answer_str = "No Answers Exist"
        for item in zip(title, contents):
            data_list.append(
                {
                    '글번호': title_num,
                    '답변 번호': '-',
                    '계층 번호': '-',
                    '제목': item[0].text,
                    '본문': item[1].text,
                    '답변': answer_str,
                    '태그': tag_str
                }
            )

    # 답변이 존재할 경우
    if answers:
        answer_num = 0    # 답변 번호 저장하는 변수
        depth_num = 0     # 계층 번호를 저장하는 변수

        for answer in answers:
            # 답변번호 증가
            answer_num += 1
            # 답변의 제목을 파싱
            answer_permalink = answer.find_all(attrs={'class': 'comment-title'})
            # 답변의 본문을 파싱
            answer_content = answer.find_all(attrs={'class': 'content'})
            # 답변의 재목과 본문을 합쳐 문자열로 형변환한다.
            answer_str = answer_permalink[0].text+answer_content[0].text
            # 답변의 계층을 분석
            parents=answer.find_parents("div",class_="indented")
            depth_num=len(parents)

            for item in zip(title, contents):
                data_list.append(
                     {
                        '글번호': title_num,
                        '답변 번호': answer_num,
                        '계층 번호': depth_num,
                        '제목': item[0].text,
                        '본문': item[1].text,
                        '답변': answer_str,
                        '태그': tag_str
                      }
                 )

    # 글번호 증가
    title_num += 1
#모든 페이지 루프 끝



# 추출한 데이터 csv파일 형태로 저장
data = pd.DataFrame(data_list)
data.to_csv('QNA_kldp.csv')