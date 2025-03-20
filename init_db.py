# pylint: disable=missing-module-docstring

import io
import duckdb as db
import pandas as pd


con = db.connect(database="data/exercises_sql_tables.duckdb",read_only=False)

#--------------------------------------------------------
# EXERCISES LIST
#--------------------------------------------------------
data={
    "theme":["cross_joins","cross_joins"],
    "exercise_name":["beverages_and_food","sizes_and_trademarks"],
    "tables":[["beverages","food_items"],["sizes,trademarks"]],
    "last_reviewed":["1990-01-01","1970-01-01"],
}
memory_state_df = pd.DataFrame(data)
con.execute("CREATE TABLE IF NOT EXISTS memory_state AS SELECT * FROM memory_state_df")


#--------------------------------------------------------
# CROSS JOIN EXERCISES
#--------------------------------------------------------
CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))
con.execute("CREATE TABLE IF NOT EXISTS food_items as SELECT * FROM food_items")

CSV3 = """
size
XS
M
L
XL
"""
size = pd.read_csv(io.StringIO(CSV3))
con.execute ("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM size")

CSV4 = """
trademark
Nike
Asphalte
Abercrombie
Lewis
"""
trademark = pd.read_csv(io.StringIO(CSV4))
con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademark")