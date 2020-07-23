import requests
import pandas as pd
from bs4 import BeautifulSoup

# url 뒤에 붙을 숫자 범위
ran = range(1, 787)
url = "https://ask.ubuntu-kr.org/?qa="

# url 뒤에 지정한 범위 내의 숫자를 붙여 배열에 저장
url_list = []
for r in ran:
    url_list.append(url + str(r))

data_list = []  # 전체 데이터 저장하는 리스트

title_num = 1  # 글번호 저장하는 변수

for url in url_list:

    # 진행 상황 파악하기 위해 링크 출력
    print(url)
    # 파싱 작업
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    # 제목 추출
    title = soup.select('body > div.qa-body-wrapper > div.qa-titles > h1 > a > span')

    # 본문 추출
    contents = soup.select(
        'div.qa-q-view-main > form > div.qa-q-view-content.qa-post-content > div')

    # 본문댓글 추출
    main_comment = soup.select(
        'body > div.qa-body-wrapper > div.qa-main-wrapper > div.qa-main > div.qa-part-q-view > div.qa-q-view > div.qa-q-view-main > div.qa-q-view-c-list > div.qa-c-list-item > form > div.qa-c-item-content.qa-post-content > div')
    # 댓글이 존재할 경우
    mcomlist = []  # 댓글 저장하는 리스트
    if main_comment:
        # 배열 형태인 댓글들을 text 형으로 전환
        for mcom in main_comment:
            mcomlist.append(mcom.text)
        # 댓글들을 구분해줄 문자열(<------->)을 사이에 추가한다.
        mcom_str = "\n\n<-------------------------------->\n\n".join(mcomlist)
    # 댓글이 존재하지 않을 경우 예외 처리
    if not main_comment:
        mcom_str = "No Comments Exist"

    # 태그 추출
    tag = soup.select(
        'div.qa-q-view-main > form > div.qa-q-view-tags > ul > li > a')
    # 태그가 존재할 경우
    tlist = []
    if tag:
        # 배열 형태인 태그들을 text 형으로 전환
        for t in tag:
            tlist.append(t.text)
        # 태그들을 구분해줄 줄바꿈을 사이에 추가한다.
        t_str = "\n".join(tlist)
    # 답변이 존재하지 않을 경우 예외 처리
    if not tag:
        t_str = "No Tags Exist"

    # 답변 추출
    answers = soup.select(
        'body > div.qa-body-wrapper > div.qa-main-wrapper > div.qa-main > div.qa-part-a-list > div.qa-a-list > div.qa-a-list-item')
    # 답변이 존재하지 않을 경우 예외 처리
    if not answers:
        answer_str = "No Answers Exist"
        for item in zip(title, contents, mcom_str, answer_str, "-", t_str):
            data_list.append(
                {
                    '글번호': title_num,
                    '제목': item[0].text,
                    '본문': item[1].text,
                    '본문 댓글': mcom_str,
                    '답변': answer_str,
                    '답변 번호': "-",
                    '댓글': item[4],
                    '태그': t_str
                }
            )

    # 답변이 존재할 경우
    if answers:
        answer_num = 0  # 답변 번호 저장하는 변수

        for answer in answers:
            # 답변번호 증가
            answer_num += 1
            # 답변의 본문 부분을 파싱
            answer_markdown = answer.find_all(attrs={'class': 'qa-a-item-content'})
            # 각각 답변에 대한 댓글 부분을 파싱
            answer_comment = answer.find_all(attrs={'class': 'qa-c-item-content'})

            # 댓글이 없을 경우
            if len(answer_comment) < 1:
                answer_comment = "no comments"

                for item in zip(title, contents, mcom_str, answer_markdown[0], answer_comment, t_str):
                    data_list.append(
                        {
                            '글번호': title_num,
                            '제목': item[0].text,
                            '본문': item[1].text,
                            '본문 댓글': mcom_str,
                            '답변': answer_markdown[0].text,
                            '답변 번호': answer_num,
                            '댓글': answer_comment,
                            '태그': t_str
                        }
                    )
            # 댓글이 있을 경우
            else:
                for ans in answer_comment:
                    # 텍스트화
                    ans = ans.text

                    for item in zip(title, contents, mcom_str, answer_markdown[0], ans, t_str):
                        data_list.append(
                            {
                                '글번호': title_num,
                                '제목': item[0].text,
                                '본문': item[1].text,
                                '본문 댓글': mcom_str,
                                '답변': answer_markdown[0].text,
                                '답변 번호': answer_num,
                                '댓글': ans,
                                '태그': t_str
                            }
                        )


    # 글번호 증가
    title_num += 1


# 추출한 데이터 csv파일 형태로 저장
data = pd.DataFrame(data_list)
data.to_csv('crawling_ubuntu.csv')