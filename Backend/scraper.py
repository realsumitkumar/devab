import psycopg2
import requests
from bs4 import BeautifulSoup

# Database connection configuration
db_config = {
    "host": "localhost",
    "database": "hackerNews",
    "user": "postgres",
    "password": "password",
}


# Function to scrape data from the website and store it in the database
def scrape_and_store_data():
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all(class_="titleline")

    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    try:
        # Start a transaction to ensure atomicity of the delete and insert operations
        conn.autocommit = False

        # Delete the existing data in the table
        cursor.execute("DELETE FROM news_articles;")

        # Insert the new data into the table
        for title in titles:
            title_text = title.text.strip()
            links = title.a
            link = links["href"]

            cursor.execute(
                "INSERT INTO news_articles (title_text, link) VALUES (%s, %s);",
                (title_text, link),
            )

        # Commit the changes and end the transaction
        conn.commit()
    except Exception as e:
        # Rollback the transaction in case of any error
        conn.rollback()
        raise e
    finally:
        # Restore autocommit mode and close the connection and cursor
        conn.autocommit = True
        cursor.close()
        conn.close()
