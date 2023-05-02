<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSON Search</title>
    <style>
        .result {
            margin-bottom: 1rem;
        }
    </style>
</head>
<body>
    <h1>Search JSON Data</h1>
    <input type="text" id="searchBox" placeholder="Search..." oninput="search()">
    <div id="results"></div>

    <script>
        function search() {
            const searchBox = document.getElementById('searchBox');
            const query = searchBox.value.trim();
            const resultsDiv = document.getElementById('results');

            if (query.length < 3) {
                resultsDiv.innerHTML = '';
                return;
            }

            const xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    const results = JSON.parse(this.responseText);
                    let html = '';

                    for (let result of results) {
                        html += `<div class="result">
                            <h3>${result.title}</h3>
                            <p>${result.url}</p>
                            <p>${result.content.substring(0, 150)}...</p>
                        </div>`;
                    }

                    resultsDiv.innerHTML = html;
                }
            };

            xhr.open("GET", `search.php?query=${encodeURIComponent(query)}`, true);
            xhr.send();
        }
    </script>
</body>
</html>
