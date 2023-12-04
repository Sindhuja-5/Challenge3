import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas

def fetch_data_from_snowflake():
    try:
        # Create a connection object
        conn = snowflake.connector.connect(
            user= "Sindhuja05",
            password="@Sindhuja5143",
            account="ncfbnjb-cl78102",
                )
        print("Connection to Snowflake account established successfully.")

        # Create a cursor object to execute SQL queries
        cur = conn.cursor()
        cur.execute(f'USE DATABASE BOOKSTORE')
        select_query = 'SELECT * FROM BOOKS_CATALOG'
        cur.execute(select_query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows, columns=columns)
        return df
        # Close the cursor and connection
    except Exception as e:
        st.error(f"Error fetching data: {e}")
    finally:
        conn.close()
    print("Connection to Snowflake account closed successfully.")
df = fetch_data_from_snowflake()


# Streamlit dashboard
st.title('Bookstore Dashboard')
st.sidebar.header("Filters:")
rating = st.sidebar.multiselect(
    "RATING",
    options = sorted(df["RATING"].unique()),
    default=sorted(df["RATING"].unique())
)

# Add a price range slider to the sidebar
price_range = st.sidebar.slider('Price Range', 
    min_value=df['PRICE'].min(), 
    max_value=df['PRICE'].max(), 
    value=(df['PRICE'].min(), df['PRICE'].max()))


df_selection = df[(df["RATING"].isin(rating)) & (df['PRICE'] >= price_range[0]) & (df['PRICE'] <= price_range[1])]
df_selection = df_selection.drop('BOOK_ID', axis=1)

# Calculate total number of books, average price and the sum of the costs of all books
total_books = len(df_selection)
average_price = df_selection['PRICE'].mean()
total_cost = df_selection['PRICE'].sum()
average_rating = df_selection['RATING'].mean()

# Displaying results in main page
left, middle, m2, right = st.columns(4)

with left:
    st.info("Books available")
    st.metric(label = "", value=f"{total_books}")

with middle:
    st.info("Avg. price of book")
    st.metric(label = "", value=f"${round(average_price, 2)}")

with right:
    st.info("Cost of inventory")
    st.metric(label = "", value=f"${round(total_cost,2)}")

with m2:
    st.info("Avg. rating")
    st.metric(label = "", value=f"{round(average_rating,2)}")

# Create tabs for rating and price distribution
tab1, tab2 = st.tabs(["Rating Distribution", "Price Distribution"])

# Main content based on selected tab
rating_distribution = px.pie(
    df_selection,
    names='RATING',
    labels={'RATING': 'Rating'}
)
# Rating Distribution tab
tab1.plotly_chart(rating_distribution, use_container_width=True)

# Price Distribution tab
price_distribution = px.histogram(df_selection, x='PRICE', nbins=20, labels={'PRICE': 'Price'})
tab2.plotly_chart(price_distribution, use_container_width=True)

#top 5 cheapest books
top_cheapest_books = df_selection.sort_values('PRICE').head(5)[['TITLE', 'RATING', 'PRICE']]
st.markdown("<h6>Top 5 cheapest books in the rating selected</h6>", unsafe_allow_html=True)
fig4 = st.table(top_cheapest_books)

#theme
hide_st_style="""
<style>
header = {visibility:hidden;}
footer = {visibility:hidden;}
</style>
"""