# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app 
st.title(":cup_with_straw: Choose your favourite smoothie:cup_with_straw:")
st.write(
    """Choose the fruits you want in custom smoothie
    """
)


name_of_order = st.text_input('Name on smoothie :')
st.write('The name on your smoothie will be:', name_of_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect (
'Choose up to 5 Ingredients:',
    my_dataframe  ,
    max_selections=5
    
)   

# new addition for fruit choices
if ingredients_list:
    ingredient_str=''
    for fruits in ingredients_list:
        ingredient_str+=fruits+' '
        st.subheader(fruits+ ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruits)
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)



if len(ingredients_list)!=0:           
    ingredint_str= ' '.join(ingredients_list)
  
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredint_str + """','"""+name_of_order+"""')"""
   

    time_to_insert=st.button('Submit Order')   
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! '+name_of_order, icon="✅")
    

    

