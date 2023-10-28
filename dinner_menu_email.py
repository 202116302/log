import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def main():
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
    table2 = soup.find_all('table', {'class': 'tblType03'})[2]

    # table 내부의 모든 <tr> 태그 찾음
    rows = table.find_all('tr')
    row2 = table2.find_all('tr')

    # 중식은 0 석식은 1인

    # 위와 마찬가지로 딕셔너리
    day_dict = {0: '월', 1: '화', 2: '수', 3: '목', 4: '금'}

    # 각 행에서 <th> 태그와 <td> 태그의 내용 가져오기
    row_lunch = rows[1]
    row_dinner = rows[2]

    row2_bf = row2[1]
    row2_zz = row2[2]
    row2_sp = row2[4]
    row2_salad = row2[7]

    column_index = datetime.today().weekday()

    day_input = day_dict.get(column_index)

    menus_per_day_l = [' '.join(str(td).replace('<br/>', ', ').replace('<td>', '').replace('</td>', '').split()) for td
                       in
                       row_lunch.find_all('td')]

    menus_per_day_d = [' '.join(str(td).replace('<br/>', ', ').replace('<td>', '').replace('</td>', '').split()) for td
                       in
                       row_dinner.find_all('td')]

    menus_per_day_bf = [' '.join(str(td).replace('<br/>', ', ').replace('<td>', '').replace('</td>', '').split()) for td
                        in
                        row2_bf.find_all('td')]

    menus_per_day_zz = [' '.join(str(td).replace('<br/>', ', ').replace('<td>', '').replace('</td>', '').split()) for td
                        in
                        row2_zz.find_all('td')]

    menus_per_day_sp = [' '.join(str(td).replace('<br/>', ', ').replace('<td>', '').replace('</td>', '').split()) for td
                        in
                        row2_sp.find_all('td')]

    menus_per_day_salad = [' '.join(str(td).replace('<br/>', ', ').replace('<td>', '').replace('</td>', '').split()) for
                           td
                           in
                           row2_salad.find_all('td')]

    data = f"{day_input}요일 \n 진수당 \n 중식 : {menus_per_day_l[column_index]} \n 석식 : {menus_per_day_d[column_index]} \n " \
           f"후생관 \n 조식 : {menus_per_day_bf[column_index]} \n 찌개 : {menus_per_day_zz[column_index]} \n 특식 : {menus_per_day_sp[column_index]} \n 샐러드: {menus_per_day_salad[column_index]}"

    issue_title = f"{day_input}요일 진수당, 후생관 메뉴 / {today_date}"
    upload_contents = data

    ### 메일 보내기

    def sendEmail(addr):
        reg = "^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$"  # 유효성 검사를 위한 정규표현식
        if re.match(reg, addr):
            smtp.sendmail(my_account, to_mail, msg.as_string())
            print("정상적으로 메일이 발송되었습니다.")
        else:
            print("받으실 메일 주소를 정확히 입력하십시오.")

    # smpt 서버와 연결
    gmail_smtp = "smtp.gmail.com"  # gmail smtp 주소
    gmail_port = 465  # gmail smtp 포트번호. 고정(변경 불가)
    smtp = smtplib.SMTP_SSL(gmail_smtp, gmail_port)

    # 로그인
    my_account = "wls5258@jbnu.ac.kr"
    my_password = "panda5258!"
    smtp.login(my_account, my_password)

    # 메일을 받을 계정
    to_mail = "wls5258@naver.com"

    # 메일 기본 정보 설정
    msg = MIMEMultipart()
    msg["Subject"] = issue_title  # 메일 제목
    msg["From"] = my_account
    msg["To"] = to_mail

    # 메일 본문 내용
    content = upload_contents
    content_part = MIMEText(content, "plain")
    msg.attach(content_part)

    # 받는 메일 유효성 검사 거친 후 메일 전송
    sendEmail(to_mail)

    # smtp 서버 연결 해제
    smtp.quit()


if __name__ == '__main__':
    main()
