import streamlit as st
import pandas as pd

def main():
    df = pd.read_csv('output/jinsu_menu.csv')
    dates = list(df['업데이트날짜'].unique())
    df_j = df.drop(['후생관_조식', '후생관_찌개', '후생관_특식', "후생관_샐러드"], axis=1)
    df_h = df.drop(['진수당_중식', '진수당_석식'], axis=1)

    st.set_page_config(layout="wide")

    st.title('진수당, 후생관 메뉴')
    for i in reversed(dates):
        st.header(f'{i}')
        st.subheader('진수당')
        df1 = df_j[df_j['업데이트날짜'] == i]
        df1 = df1.drop('업데이트날짜', axis=1)
        st.table(df1.style.hide_index())
        st.subheader('후생관')
        df2 = df_h[df_h['업데이트날짜'] == i]
        df2 = df2.drop('업데이트날짜', axis=1)
        st.table(df2.style.hide_index())







if __name__ == '__main__':
    main()