# pylint: disable=missing-module-docstring
import ast
import io

import duckdb as db
import pandas as pd
import streamlit as st


con = db.connect(database="data/exercises_sql_tables.duckdb",read_only=False)

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review ?",
        ("cross_joins", "GroupBy", "window_functions"),
        index=None,
        placeholder="Select a theme..",
    )

    st.write("You selected:", theme)
    exercise  = con.execute(f"SELECT * from memory_state WHERE theme='{theme}'").df().sort_values("last_reviewed").reset_index()
    st.write(exercise)

    #on recupere la solution de l exercice
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()
    solution_df = con.execute(answer).df()


st.header("Enter your code")
query = st.text_area(label="Votre code SQL ici", key="user_input")

if query:
    result = con.execute(query).df()
    st.dataframe(result)

    # comparaison nombre de colonnes
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
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
    exercise_tables=exercise.loc[0, "tables"]

    for table in exercise_tables:
        st.write(f"Table: {table}")
        df_table = con.execute(f"SELECT * from {table}").df()
        st.dataframe(df_table)

with tab2:
    st.write(answer)