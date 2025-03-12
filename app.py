import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Connection details for TiDB Cloud
username = '3YKstZXrasws9wp.root'
password = '2tViyw42uqIpBKko'
host = 'gateway01.ap-southeast-1.prod.aws.tidbcloud.com'
port = 4000
database = 'proj_guvi'
ssl_ca_path = r'C:/Users/JANANI V/proj_1_guvi/isrgrootx1 (1).pem'

# Create SQLAlchemy engine
ssl_ca_path = r'C:/Users/JANANI V/proj_1_guvi/isrgrootx1 (1).pem'
connection_string = f'mysql+pymysql://3YKstZXrasws9wp.root:2tViyw42uqIpBKko@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/proj_guvi?ssl_ca={ssl_ca_path}'
engine = create_engine(connection_string)

# Define the queries
queries_set_1 = {
    "Top 10 highest revenue generating products (LEFT JOIN)": """
        SELECT orders.product_id, SUM(sale_price) AS total_revenue
        FROM orders
        LEFT JOIN products ON orders.product_id = products.product_id
        GROUP BY orders.product_id
        ORDER BY total_revenue DESC
        LIMIT 10;
    """,
    "Top 5 cities with the highest profit margins": """
        SELECT orders.city, SUM(products.profit) AS total_profit
        FROM orders
        JOIN products ON orders.product_id = products.product_id
        GROUP BY orders.city
        ORDER BY total_profit DESC
        LIMIT 5;
    """,
    "Total discount given for each product": """
        SELECT orders.product_id, SUM(products.discount) AS total_discount
        FROM orders
        JOIN products ON orders.product_id = products.product_id
        GROUP BY orders.product_id
        ORDER BY total_discount DESC;
    """,
    "Average sale price per product": """
        SELECT orders.product_id, AVG(products.sale_price) AS average_sale_price
        FROM orders
        JOIN products ON orders.product_id = products.product_id
        GROUP BY orders.product_id
        ORDER BY average_sale_price DESC;
    """,
    "City with the highest average sale price": """
        SELECT orders.city, AVG(products.sale_price) AS average_sale_price
        FROM orders
        JOIN products ON orders.product_id = products.product_id
        GROUP BY orders.city
        ORDER BY average_sale_price DESC
        LIMIT 1;
    """,
    "Total profit per product": """
        SELECT orders.product_id, SUM(products.profit) AS total_profit
        FROM orders
        JOIN products ON orders.product_id = products.product_id
        GROUP BY orders.product_id
        ORDER BY total_profit DESC;
    """,
    "Top 3 segments with the highest quantity of orders": """
        SELECT orders.segment, COUNT(orders.order_id) AS total_orders
        FROM orders
        GROUP BY orders.segment
        ORDER BY total_orders DESC
        LIMIT 3;
    """,
    "Average discount percentage given per city": """
        SELECT orders.city, AVG(products.discount_percent) AS average_discount_percent
        FROM orders
        JOIN products ON orders.product_id = products.product_id
        GROUP BY orders.city
        ORDER BY average_discount_percent DESC;
    """,
    "Product with the highest total profit": """
        SELECT orders.product_id, SUM(products.profit) AS total_profit
        FROM orders
        JOIN products ON orders.product_id = products.product_id
        GROUP BY orders.product_id
        ORDER BY total_profit DESC
        LIMIT 1;
    """,
    "Total revenue generated per year": """
        SELECT YEAR(orders.order_date) AS year, SUM(products.sale_price) AS total_revenue
        FROM orders
        JOIN products ON orders.product_id = products.product_id
        GROUP BY YEAR(orders.order_date)
        ORDER BY year;
    """
}

queries_set_2 = {
    "Top 5 products with the highest profit margins": """
        SELECT orders.product_id, SUM(products.profit) AS total_profit
        FROM orders
        JOIN products ON orders.product_id = products.product_id
        GROUP BY orders.product_id
        ORDER BY total_profit DESC
        LIMIT 5;
    """,
    "Total revenue for each segment": """
        SELECT orders.segment, SUM(products.sale_price) AS total_revenue
        FROM orders
        JOIN products ON orders.product_id = products.product_id
        GROUP BY orders.segment
        ORDER BY total_revenue DESC;
    """,
    "Average profit per product": """
        SELECT orders.product_id, AVG(products.profit) AS average_profit
        FROM orders
        JOIN products ON orders.product_id = products.product_id
        GROUP BY orders.product_id
        ORDER BY average_profit DESC;
    """,
    "Top 5 cities with the highest total sales": """
        SELECT orders.city, SUM(products.sale_price) AS total_sales
        FROM orders
        JOIN products ON orders.product_id = products.product_id
        GROUP BY orders.city
        ORDER BY total_sales DESC
        LIMIT 5;
    """,
    "Total number of orders per month": """
        SELECT YEAR(orders.order_date) AS year, MONTH(orders.order_date) AS month, COUNT(orders.order_id) AS total_orders
        FROM orders
        GROUP BY YEAR(orders.order_date), MONTH(orders.order_date)
        ORDER BY year, month;
    """,
    "Average discount percentage per product": """
        SELECT orders.product_id, AVG(products.discount_percent) AS average_discount_percent
        FROM orders
        JOIN products ON orders.product_id = products.product_id
        GROUP BY orders.product_id
        ORDER BY average_discount_percent DESC;
    """,
    "Top 3 products with the highest total sales in each city": """
        SELECT orders.city, orders.product_id, SUM(products.sale_price) AS total_sales
        FROM orders
        JOIN products ON orders.product_id = products.product_id
        GROUP BY orders.city, orders.product_id
        ORDER BY orders.city, total_sales DESC
        LIMIT 3;
    """,
    "Total profit per segment": """
        SELECT orders.segment, SUM(products.profit) AS total_profit
        FROM orders
        JOIN products ON orders.product_id = products.product_id
        GROUP BY orders.segment
        ORDER BY total_profit;
    """,
    "Product with the highest average sale price": """
        SELECT orders.product_id, AVG(products.sale_price) AS average_sale_price
        FROM orders
        JOIN products ON orders.product_id = products.product_id
        GROUP BY orders.product_id
        ORDER BY average_sale_price DESC
        LIMIT 1;
    """,
    "Total revenue generated per city": """
        SELECT orders.city, SUM(products.sale_price) AS total_revenue
        FROM orders
        JOIN products ON orders.product_id=products.product_id
        GROUP BY orders.city
        ORDER BY total_revenue DESC;
    """
}

# Streamlit app

st.markdown(
    '<h1 style="color: blue;">SQL Query Insights</h1>',
    unsafe_allow_html=True
)
# Dropdown to select query set
query_set = st.selectbox("Select a query set", ["Set 1", "Set 2"])

# Select the appropriate query set
if query_set == "Set 1":
    queries = queries_set_1
else:
    queries = queries_set_2

# Dropdown to select query
query_name = st.selectbox("Select a query", list(queries.keys()))

# Execute the selected query
query = queries[query_name]
result = pd.read_sql(query, con=engine)

# Display the result
st.write(result)



# Allow user to select only numerical columns to plot
columns = st.multiselect(
    "Select columns to plot",
    options=result.select_dtypes(include=['number']).columns,  # Only show numerical columns
    default=result.select_dtypes(include=['number']).columns  # Preselect numerical columns
)

# Create a subset of the DataFrame with the selected columns
selected_data = result[columns]

# Display the result in different chart types
chart_type = st.selectbox("Select chart type", ["Bar Chart", "Line Chart", "Area Chart"])

if chart_type == "Bar Chart":
    st.bar_chart(selected_data)
elif chart_type == "Line Chart":
    st.line_chart(selected_data)
elif chart_type == "Area Chart":
    st.area_chart(selected_data)



# Add some styling to make the background colorful
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f0f0;
        background-image: linear-gradient(135deg, #f0f0f0 25%, #e0e0e0 25%, #e0e0e0 50%, #f0f0f0 50%, #f0f0f0 75%, #e0e0e0 75%, #e0e0e0 100%);
        background-size: 28.28px 28.28px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
