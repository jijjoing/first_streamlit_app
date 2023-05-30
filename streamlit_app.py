import streamlit
import pandas 
import requests
import snowflake.connector
from urllib.error import URLError

# streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 % Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt") # S3 데이터 가지고 오기
my_fruit_list = my_fruit_list.set_index('Fruit') # 과일 이름으로 선택할 수 있도록 index 설정

# Let's put a pick list here so they can pick the fruit they want to include 
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index)) # 설정된 인덱스를 선택 가능하도록 설정
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries']) # 픽스 인덱스 값 설정
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
# streamlit.dataframe(my_fruit_list) # 저장된 S3 데이터를 데이터프레임으로 설정
streamlit.dataframe(fruits_to_show) # 픽스 데이터가 설정된 버전으로 변경

# New Section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi') # 텍스트 입력 상자
streamlit.write('The user entered ', fruit_choice) # API 일부 호출

# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon") # watermelon json 파일 불러오기
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# streamlit.text(fruityvice_response.json()) # just writes the data to the screen # 불러온 json 파일 형식 그대로 출력

# [fruityvice_normalized]변수에 정규화된 json 파일을 저장
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# 저장한 변수를 데이터프레임으로 변경
streamlit.dataframe(fruityvice_normalized)

# don't run anything past here while we troubleshoot
streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)
# streamlit.text("Hello from Snowflake:")
# streamlit.text("The fruit load list contains:")
# streamlit.text(my_data_row)

add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit') # 텍스트 입력 상자

streamlit.write('Thanks for adding ', add_my_fruit)
# This will not correctly, but just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
