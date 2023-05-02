<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSON Search</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }

        h1 {
            background-color: #4CAF50;
            color: white;
            padding: 1rem;
            margin-bottom: 2rem;
        }

        input[type="text"] {
            display: block;
            width: 100%;
            padding: 0.5rem;
            font-size: 1rem;
            box-sizing: border-box;
        }

        #results {
            padding: 1rem;
        }

        .result {
            margin-bottom: 1rem;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 1rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
        }

        .result h3 {
            margin-top: 0;
            color: #4CAF50;
        }

        .result p {
            margin: 0.5rem 0;
        }

        .result p:first-child {
            font-weight: bold;
        }

        .result p:last-child {
            color: #777;
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