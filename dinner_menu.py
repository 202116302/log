import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from pytz import timezone
from github_utils import get_github_repo, upload_github_issue


def main():
    # github action 세팅 ##
    # access_token = os.environ['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']
    access_token = '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'
    repository_name = "log"

    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    today_date = today.strftime("%Y년 %m월 %d일")

    url = "https://sobi.chonbuk.ac.kr/menu/week_menu.php"

    response = requests.get(url)
    html_text = response.content.decode('utf-8')  # UTF-8로 디코딩
    soup = BeautifulSoup(html_text, 'html.parser')
    # 홈페이지 가서 f12누르면 홈페이지 구성요소에 대한 정보가 나옴.

    # "tblType03" 클래스를 가진 table 찾기
    table = soup.find('table', {'class': 'tblType03'})

    # table 내부의 모든 <tr> 태그 찾음
    rows = table.find_all('tr')
    # 중식은 0 석식은 1인

    # 위와 마찬가지로 딕셔너리
    day_dict = {0: '월', 1: '화', 2: '수', 3: '목', 4: '금'}

    # 각 행에서 <th> 태그와 <td> 태그의 내용 가져오기
    row_lunch = rows[1]
    row_dinner = rows[2]

    column_index = datetime.today().weekday()

    day_input = day_dict.get(column_index)

    menus_per_day_l = [' '.join(str(td).replace('<br/>', ', ').replace('<td>', '').replace('</td>', '').split()) for td
                       in
                       row_lunch.find_all('td')]

    menus_per_day_d = [' '.join(str(td).replace('<br/>', ', ').replace('<td>', '').replace('</td>', '').split()) for td
                       in
                       row_dinner.find_all('td')]

    data = f"{day_input}요일 중식 : {menus_per_day_l[column_index]} / 석식 : {menus_per_day_d[column_index]}"

    print(data)

    issue_title = f"{day_input}요일 진수원 메뉴 / {today_date}"
    upload_contents = data
    repo = get_github_repo(access_token, repository_name)
    upload_github_issue(repo, issue_title, upload_contents)


if __name__ == '__main__':
    main()
