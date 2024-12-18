# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie!")
st.write(
    """Choose the Fruits you want in your smoothie!
    """)

# Get the current credentials

cnx = st.connection("snowflake")
session = cnx.session()

customer_name = st.text_input('Name on Smoothie')
#st.write(customer_name)

fruit_data = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data = fruit_data,use_container_width=True)

# convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df = fruit_data.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingrrdiant_list = st.multiselect(
    'Choose upto 5 fruits',
    fruit_data,
    max_selections = 5
)

sunmit_order = st.button('Submit Order')

if ingrrdiant_list and customer_name:
    #st.write('Your selected : ',ingrrdiant_list)
    #st.text(ingrrdiant_list)
       
    ingredients_string =  ''

    for each_fruit in ingrrdiant_list:
        ingredients_string += each_fruit + ' ';

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', each_fruit,' is ', search_on, '.')

        if search_on:
            smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
            st.text(each_fruit + ' Nutrision Intormation')
            sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        else: 
            st.text('No Nutrision Intormation found')


    #st.write('Your selected : ',ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','"""+customer_name +"""')"""

    #st.write(my_insert_stmt)

    if ingredients_string and sunmit_order:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+ customer_name +'!', icon="✅")
        st.stop()




#contact = st.selectbox(
#    'How would you like to be contected?',
#    ('Email','Home Phone','Mobile Phone'))


#fruit = st.selectbox(
#    'What is your favourite Fruit?',
#    ('Mango','Orange','Apple','Banana','Staberies','Peaches'))




