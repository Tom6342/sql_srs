# pylint: disable=missing-module-docstring
import ast
import os
import logging
import duckdb as db
import pandas as pd
import streamlit as st
from datetime import date, timedelta, datetime

if "data" not in os.listdir():
    logging.debug(os.listdir())
    logging.debug("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

con = db.connect(database="data/exercises_sql_tables.duckdb",read_only=False)

def check_users_solution(user_query: str) -> None:
    """
    Checks that user SQL query is correct by :
    1 : checking the columns
    2 : checking the values
    :param user_query: a string containing the query inserted by the user

    """
    result = con.execute(user_query).df()
    st.dataframe(result)

    # comparaison nombre de colonnes
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
        if result.compare(solution_df).shape == (0, 0):
            st.write("correct !")
            st.balloons()
    except KeyError as e:
        st.write("Some columns are missing")

        # comparaison nombre de lignes
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"result has a {n_lines_difference} lines difference with the solution_df"
        )

with st.sidebar:
    list_themes = con.execute("SELECT DISTINCT theme from memory_state").df()

    theme = st.selectbox(
        "What would you like to review ?",
        list_themes["theme"].unique(),
       # ("cross_joins", "GroupBy", "window_functions"),
        index=None,
        placeholder="Select a theme..",
    )
    if theme:
        st.write("You selected:", theme)
        select_exercise_query = f"SELECT * from memory_state WHERE theme='{theme}'"
    else:
        select_exercise_query = "SELECT * from memory_state"

    exercise = (
        con.execute(select_exercise_query)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )

    st.write(exercise)
    #on recupere la solution de l exercice
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()
    solution_df = con.execute(answer).df()
st.header("Enter your code")
query = st.text_area(label="Votre code SQL ici", key="user_input")

if query:
   check_users_solution(query)

for n_days in [2, 7, 21]:
    if st.button(f'revoir dans {n_days} jours'):
        next_review = date.today() + timedelta(days=n_days)
        con.execute(f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercise_name = '{exercise_name}")
        st.rerun()

if st.button('Reset'):
    con.execute(f"UPDATE memory_state SET last_reviewed = '1970-01-01")
    st.rerun()

tab1, tab2 = st.tabs(["Tables", "Solution"])

with tab1:
    exercise_tables=exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"Table: {table}")
        df_table = con.execute(f"SELECT * from {table}").df()
        st.dataframe(df_table)

with tab2:
    st.write(answer)
