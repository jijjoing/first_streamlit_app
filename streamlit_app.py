import streamlit

# streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 % Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas 
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt") # S3 데이터 가지고 오기
my_fruit_list = my_fruit_list.set_index('Fruit') # 과일 이름으로 선택할 수 있도록 index 설정

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# streamlit.dataframe(my_fruit_list) # 저장된 S3 데이터를 데이터프레임으로 설정
streamlit.dataframe(fruits_to_show) # 픽스 데이터가 설정된 버전으로 변경

streamlit.header('Fruityvice Fruit Advice!')

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi') # 텍스트 입력 상자
streamlit.write('The user entered ', fruit_choice) # API 일부 호출

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# [fruityvice_normalized]변수에 정규화된 json 파일을 저장
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# 저장한 변수를 데이터프레임으로 변경
streamlit.dataframe(fruityvice_normalized)


# snowflake 파이썬 커넥터 연결
# import snowflake.connector
