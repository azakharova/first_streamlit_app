import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title('New healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Pick list to pick the fruit to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# New section to display Fruitvice API response
streamlit.header('Fruitvice Fruit Advice!')
fruit_choice = streamlit.text_input("What fruit do you want to know about?", "kiwi")
streamlit.write("You selected", fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# Normalize the API response
fruitvice_normalize = pandas.json_normalize(fruityvice_response.json())
fruitvice_normalize = fruitvice_normalize.set_index('name')
streamlit.dataframe(fruitvice_normalize) # Display the API response on the page

# Snowflake connection
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:  ")
streamlit.dataframe(my_data_rows)

fruit_add = streamlit.text_input("What fruit do you want to add to the list?", "jackfruit")
my_cur.execute("insert into fruit_load_list values ('" + fruit_add + "')")
streamlit.text("Thank you for adding " + fruit_add + " to the list")

# this does not work correctly yet
my_cur.execute("insert into fruit_load_list values ('from streamlit')")