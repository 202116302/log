import streamlit as st
import pandas as pd


def count_menu(cell, menu):
    return cell.count(f'{menu}')


def count_menu2(cell, menu, menu2):
    return cell.count(f'{menu}') + cell.count(f'{menu2}')


def count_menu_sum(df, menu):
    m_list = []
    for i in menu:
        m_list.append(df.applymap(count_menu, menu=i).values.sum())
    return m_list


def main():
    df = pd.read_csv('output/jinsu_menu.csv')
    dates = list(df['업데이트날짜'].unique())
    df_j = df.drop(['후생관_조식', '후생관_찌개', '후생관_특식', "후생관_샐러드"], axis=1)
    df_h = df.drop(['진수당_중식', '진수당_석식'], axis=1)

    soup = ['국', '찌개', '탕']

    chan = ['무침', '볶음']

    result_js = count_menu_sum(df_j, soup)
    result_hs = count_menu_sum(df_h, soup)
    result_jc = count_menu_sum(df_j, chan)
    result_hc = count_menu_sum(df_h, chan)

    # 돼지, 닭, 소 순서
    result_hm = []
    result_hm.append(df_h.applymap(count_menu2, menu='돈', menu2='돼지').values.sum())
    result_hm.append(df_h.applymap(count_menu2, menu='닭', menu2='치킨').values.sum())
    result_hm.append(df_h.applymap(count_menu, menu='소').values.sum())
    result_jm = []
    result_jm.append(df_j.applymap(count_menu2, menu='돈', menu2='돼지').values.sum())
    result_jm.append(df_j.applymap(count_menu2, menu='닭', menu2='치킨').values.sum())
    result_jm.append(df_j.applymap(count_menu, menu='소').values.sum())

    df_s = pd.DataFrame([result_js, result_hs], columns=soup)
    df_c = pd.DataFrame([result_jc, result_hc], columns=chan)
    df_m = pd.DataFrame([result_jm, result_hm], columns=['돼지', '닭', '소'])

    df_s['loc'] = ['진수당', '후생관']
    df_c['loc'] = ['진수당', '후생관']
    df_m['loc'] = ['진수당', '후생관']

    df_s = df_s.set_index('loc')
    df_c = df_c.set_index('loc')
    df_m = df_m.set_index('loc')

    print(df_s)

    st.set_page_config(layout="wide")

    st.title('진수당, 후생관 메뉴')
    for i in reversed(dates):
        st.header(f'{i}')
        st.subheader('진수당')
        df1 = df_j[df_j['업데이트날짜'] == i]
        df1 = df1.drop('업데이트날짜', axis=1)
        st.table(df1)
        st.subheader('후생관')
        df2 = df_h[df_h['업데이트날짜'] == i]
        df2 = df2.drop('업데이트날짜', axis=1)
        st.table(df2)

    st.title('메뉴 분석')

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader('국(국, 찌개, 탕)')

        st.bar_chart(df_s, width=400, use_container_width=False)

    with col2:
        st.subheader('고기(돼지, 닭, 소)')

        st.bar_chart(df_m, width=400, use_container_width=False)

    with col3:
        st.subheader('반찬(무침, 볶음)')

        st.bar_chart(df_c, width=400, use_container_width=False)


if __name__ == '__main__':
    main()
