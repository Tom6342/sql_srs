import io
import streamlit as st
import pandas as pd
import duckdb as db


def my_func():
    """
    coucou

    :return:
    """
    print()

CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))

ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""
solution_df = db.sql(ANSWER_STR).df()

with st.sidebar:
    option = st.selectbox(
        "What would you like to review ?",
        ("Joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Select a theme..",
    )

    st.write("You selected:", option)

st.header("Enter your code")
query = st.text_area(label="Votre code SQL ici", key="user_input")

if query:
    result = db.sql(query).df()
    st.dataframe(result)

    # comparaison nombre de colonnes

    try:
        result = result[solution_df.columns]
        st.write("Some columns are missing")
    except KeyError as e:
        st.write("Some columns are missing")

    # comparaison nombre de lignes
    n_lines_difference = result.shape[0] - solution_df.shape[0]

    if n_lines_difference != 0:
        st.write(
            f"result has a {n_lines_difference} lines difference with the solution_df"
        )


tab1, tab2 = st.tabs(["Tables", "Solution"])

with tab1:
    st.write("Table: beverages")
    st.dataframe(beverages)
    st.write("Table: food_items")
    st.dataframe(food_items)
    st.write("expected:")
    st.dataframe(solution_df)

with tab2:
    st.write(ANSWER_STR)
