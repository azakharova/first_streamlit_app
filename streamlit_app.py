import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('New healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



# import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

## Pick list to pick the fruit to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

## Display the table on the page.
streamlit.dataframe(fruits_to_show)

## function tu return api response
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

## New section to display fruityvice API response
streamlit.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = streamlit.text_input("What fruit do you want to know about?")
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information about")
    else:
        back_from_fruityvice = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_fruityvice)

except URLError as e:
    streamlit.error(
        """
        **This demo requires internet access.**

        Connection error: %s
        """
        % e.reason
    )



# import snpwflake.connector
streamlit.header("The fruit load list contains:  ")

## function to return the fruit load list from snowflake
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

## Add a button to load the fruit
if streamlit.button("Get Fruit Load List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

## Allow the end user to add a fruit to the list
def insert_row_snowflake(fruit_to_add):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('" + fruit_to_add + "')")
        return "Thank you for adding " + fruit_to_add + " to the list"
    
add_my_fruit = streamlit.text_input("What fruit do you want to add to the list?")
if streamlit.button("Add a Fruit to the List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)