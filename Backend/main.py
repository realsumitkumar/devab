from flask import Flask, jsonify
import psycopg2
from flask_cors import CORS
from scraper import scrape_and_store_data

app = Flask(__name__)
CORS(app)

db_config = {
    "host": "localhost",
    "database": "hackerNews",
    "user": "postgres",
    "password": "password",
}


# Endpoint to retrieve data from the database
@app.route("/api/news_articles", methods=["GET"])
def get_news_articles():
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        sql_query = "SELECT title_text, link FROM news_articles;"
        cursor.execute(sql_query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        results = [{"title_text": row[0], "link": row[1]} for row in data]

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Call the scrape_and_store_data() function to scrape and store data when the app starts
    scrape_and_store_data()

    app.run(debug=True)
