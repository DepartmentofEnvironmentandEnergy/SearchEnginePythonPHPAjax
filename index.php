<!-- // index.php -->
<!DOCTYPE html>
<html>
<head>
	<title>Search Example</title>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
	<script>
		$(document).ready(function() {
			$("#search-box").on('input', function() {
				var query = $(this).val();
				var results = $("#results");
				results.empty();
				if (!query) {
					results.append("<p>Please enter a search query.</p>");
					return;
				}
				results.append("<div class=\"loader\"></div>");
				$.ajax({
					url: "search.php",
					method: "GET",
					data: {query: query},
					dataType: "json",
					success: function(data) {
						results.empty();
						if (data.length === 0) {
							results.append("<p>No results found.</p>");
						} else {
							$.each(data, function(index, page) {
								results.append("<h3><a href=\"" + page.url + "\">" + page.title + "</a></h3>");
								results.append("<p>" + page.content + "</p>");
							});
						}
					},
					error: function() {
						results.empty();
						results.append("<p>Error searching for results.</p>");
					},
					complete: function() {
						$(".loader").remove();
					}
				});
			});
		});
	</script>
	<style>
		.loader {
			border: 16px solid #f3f3f3;
			border-top: 16px solid #3498db;
			border-radius: 50%;
			width: 120px;
			height: 120px;
			animation: spin 2s linear infinite;
			margin: auto;
		}
		@keyframes spin {
			0% { transform: rotate(0deg); }
			100% { transform: rotate(360deg); }
		}
	</style>
</head>
<body>
	<form id="search-form">
		<label for="search-box">Search:</label>
		<input type="text" id="search-box" name="query">
	</form>
	<div id="results"></div>
</body>
</html>