// Function to fetch data from the Flask API and update the news items
function fetchNewsData() {
    fetch('http://127.0.0.1:5000/api/news_articles')
        .then(response => response.json())
        .then(data => {
            const newsList = document.getElementById('news-list');
            let newsHTML = '';

            data.forEach(newsItem => {
                const title = newsItem.title_text;
                const link = newsItem.link;

                // Create the HTML for each news item dynamically
                const newsItemHTML = `
                    <a href="${link}" class="columnslist-group-item list-group-item-action py-2 lh-sm rows" aria-current="true">
                        <div class="d-flex w-100 align-items-center justify-content-between mx-2">
                            <strong class="mb-2">${title}</strong>
                        </div>
                    </a>
                `;

                newsHTML += newsItemHTML;
            });

            // Update the news list with the fetched data
            newsList.innerHTML = newsHTML;
        })
        .catch(error => console.error('Error fetching news data:', error));
}

// Call the fetchNewsData() function when the page loads
fetchNewsData();
