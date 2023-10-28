import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from pytz import timezone
import pandas as pd

def main():
    dirname = 'output'
    if not os.path.exists(dirname):
        os.mkdir(dirname)


    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    today_date = today.strftime("%Y년 %m월 %d일")

    url = "https://sobi.chonbuk.ac.kr/menu/week_menu.php"

    response = requests.get(url)
    html_text = response.content.decode('utf-8')  # UTF-8로 디코딩
    soup = BeautifulSoup(html_text, 'html.parser')
    # 홈페이지 가서 f12누르면 홈페이지 구성요소에 대한 정보가 나옴.

    # "tblType03" 클래스를 가진 table 찾기 진수당
    table = soup.find('table', {'class': 'tblType03'})
    # "tblType03" 클래스를 가진 table 찾기 후생관
    table2 = soup.find_all('table', {'class': 'tblType03'})[2]

    # table 내부의 모든 <tr> 태그 찾음
    rows = table.find_all('tr')
    # 후생관
    row2 = table2.find_all('tr')



    # 위와 마찬가지로 딕셔너리
    day_dict = {0: '월', 1: '화', 2: '수', 3: '목', 4: '금'}

    # 각 행에서 <th> 태그와 <td> 태그의 내용 가져오기
    # 진수당 중식, 석식
    row_lunch = rows[1]
    row_dinner = rows[2]

    # 후생관 조식, 찌개, 특식, 샐러드
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

    menus_per_day_salad = [' '.join(str(td).replace('<br/>', ', ').replace('<td>', '').replace('</td>', '').split()) for td
                        in
                        row2_salad.find_all('td')]


    # 실행 시키면 메뉴 CSV 파일로 저장

    # data = f"{day_input}요일 \n 중식 : {menus_per_day_l[column_index]} \n 석식 : {menus_per_day_d[column_index]}"

    df = pd.DataFrame({'요일': [day_dict[0], day_dict[1], day_dict[2], day_dict[3], day_dict[4]],
                       '진수당_중식': [menus_per_day_l[0], menus_per_day_l[1], menus_per_day_l[2], menus_per_day_l[3],
                              menus_per_day_l[4]],
                       '진수당_석식': [menus_per_day_d[0], menus_per_day_d[1], menus_per_day_d[2], menus_per_day_d[3],
                              menus_per_day_d[4]],
                       '후생관_조식': [menus_per_day_bf[0], menus_per_day_bf[1], menus_per_day_bf[2], menus_per_day_bf[3],
                                  menus_per_day_bf[4]],
                       '후생관_찌개': [menus_per_day_zz[0], menus_per_day_zz[1], menus_per_day_zz[2], menus_per_day_zz[3],
                                  menus_per_day_zz[4]],
                       '후생관_특식': [menus_per_day_sp[0], menus_per_day_sp[1], menus_per_day_sp[2], menus_per_day_sp[3],
                                  menus_per_day_sp[4]],
                       '후생관_샐러드': [menus_per_day_salad[0], menus_per_day_salad[1], menus_per_day_salad[2], menus_per_day_salad[3],
                                  menus_per_day_salad[4]],
                       })

    df['업데이트날짜'] = today_date

    if not os.path.exists('output/jinsu_menu.csv'):
        df.to_csv('output/jinsu_menu.csv', encoding='utf-8-sig', index=False)

    else:
        df_origin = pd.read_csv('output/jinsu_menu.csv')
        df2 = pd.concat([df_origin, df])
        df2 = df2.drop_duplicates()
        df2.to_csv('output/jinsu_menu.csv', encoding='utf-8-sig', index=False)






if __name__ == '__main__':
    main()
