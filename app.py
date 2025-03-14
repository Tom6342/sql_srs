import streamlit as st
import pandas as pd
import duckdb as db
import io

csv = '''
beverage,price
orange juice,2.5
Expresso,2
Tea,3
'''
beverages = pd.read_csv(io.StringIO(csv))

csv2 = '''
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
'''
food_items = pd.read_csv(io.StringIO(csv2))

answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""
solution = db.sql(answer).df()

with st.sidebar:
    option = st.selectbox(
     "What would you like to review ?",
     ("Joins","GroupBy", "Windows Functions"),
     index=None,
     placeholder="Select a theme..",
    )

    st.write("You selected:", option )

st.header("Enter your code")
query = st.text_area(label="Votre code SQL ici", key="user_input")

if query:
    result = db.sql(query).df()
    st.dataframe(result)
    
tab1, tab2 = st.tabs(["Tables", "Solution"])

with tab1:
    st.write("Table: beverages")
    st.dataframe(beverages)
    st.write("Table: food_items")
    st.dataframe(food_items)
    st.write("expected:")
    st.dataframe(solution)

with tab2:
    st.write(answer)




