import os
import pandas as pd
import sqlite3
import streamlit as st

def load_data():
    # 現在のファイルのディレクトリを取得
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # データベースファイルへのパスを構築
    db_path = os.path.join(current_dir, 'property.db')
    # データベースに接続
    conn = sqlite3.connect(db_path)
    # SQLクエリを実行し、結果をDataFrameに読み込む
    query = "SELECT * FROM properties"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

df = load_data()



# 希望条件
# 区リスト
wards_list = [
    '千代田区', '中央区', '港区', '新宿区', '文京区', '台東区', '墨田区', '江東区',
    '品川区', '目黒区', '大田区', '世田谷区', '渋谷区', '中野区', '杉並区', '豊島区', 
    '北区', '荒川区', '板橋区', '練馬区', '足立区', '葛飾区', '江戸川区'
    ]
# 間取りリスト
floor_list = [
    '2K', '2DK', '2LDK', '3K', '3DK', '3LDK', '3SLDK', '4K', '4SK', '4SDK'
    ]


# 会員登録・Loginボタンを画面右上に配置
col1, col2, col3 = st.columns([9,2,2])
with col2:
    st.button('会員登録', type='secondary')
with col3:
    st.button('Login', type='secondary')

# タイトル
st.title('物件情報検索アプリ')
# アプリ概要説明
st.write('あなたの家探しを一瞬で。忙しい毎日に最適な住まいを。')

# 以下、サイドバーで希望の条件を入力する枠を用意
st.sidebar.title('希望条件を入力してください')

# 対象区
st.sidebar.text('1.対象エリア')
wards_select = st.sidebar.multiselect('希望の対象エリアを選択してください（複数選択可）', wards_list)

# 賃料
st.sidebar.text('2.賃料')
min_rent, max_rent = st.sidebar.slider(
    '賃料（万円）の範囲を入力してください',
    min_value=0,
    max_value=30,
    value=(0, 30))
min_rent_yen = min_rent * 10000
max_rent_yen = max_rent * 10000

# 駅徒歩
st.sidebar.text('3.駅徒歩')
min_walk_time, max_walk_time = st.sidebar.slider(
    '駅徒歩時間（分）の範囲を入力してください',
    min_value=0,
    max_value=30,
    value=(0, 30))

# 間取り
st.sidebar.text('4.間取り')
floor_select = st.sidebar.multiselect('希望の間取りを選択してください（複数選択可）', floor_list)

# 築年数
st.sidebar.text('5.築年数')
min_age, max_age = st.sidebar.slider(
    '築年数の範囲を入力してください',
    min_value=0,
    max_value=100,
    value=(0, 50))

# 占有面積
st.sidebar.text('6.占有面積')
min_menseki, max_menseki = st.sidebar.slider(
    '占有面積（m2）の範囲を入力してください',
    min_value=0,
    max_value=150,
    value=(0, 75))

# 検索ボタンを設置
button = st.sidebar.button('検索', type='primary')

# 検索条件でデータを絞り込み、結果を df_search に代入
df_search = df.query(
    f'(ward in {wards_select}) and ({min_rent_yen} <= fee <= {max_rent_yen}) and ({min_walk_time} <= access1_walking_minutes <= {max_walk_time}) and (floor_plan in {floor_select}) and ({min_age} <= age <= {max_age}) and ({min_menseki} <= area <= {max_menseki})')

# 検索結果のヒット件数を取得
hit = len(df_search)

# map用に緯度、経度データだけを df_loc に代入。geopyで緯度経度取得できなかった欠損地は削除。
df_loc = df_search[['lat', 'lon']].dropna()

# df_searchのカラム名を全て日本語に直す
df_search.columns = ['物件名', '住所', '築年数', '構造', '階数', '賃料', '管理費', '敷金', '礼金', '間取り', '占有面積', '最寄駅路線1', '最寄駅1', '駅徒歩1', '最寄駅路線2', '最寄駅2', '駅徒歩2', '最寄駅路線3', '最寄駅3', '駅徒歩3', '緯度', '経度']

# 検索ボタンを押した際に、結果を表示
if button:
    st.write('■ 検索結果')
    st.write(f'▼ ヒット件数：{hit}件')
    st.write('▼ 物件一覧：')
    st.dataframe(df_search, width=700, height=300)
    st.write('▼ マップ：')
    st.map(df_loc)
