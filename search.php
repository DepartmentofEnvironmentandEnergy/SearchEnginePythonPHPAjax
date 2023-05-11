<!-- // search.php -->
<?php

header('Content-Type: application/json');

$query = $_GET['query'] ?? '';
$query = strtolower(trim($query));

$data = [];
$json = file_get_contents('website_data.json');

if ($json === false) {
    die('Error loading website data');
}

$data = json_decode($json, true);

if ($data === null && json_last_error() !== JSON_ERROR_NONE) {
    switch (json_last_error()) {
        case JSON_ERROR_DEPTH:
            $error = 'Maximum stack depth exceeded';
            break;
        case JSON_ERROR_STATE_MISMATCH:
            $error = 'Underflow or the modes mismatch';
            break;
        case JSON_ERROR_CTRL_CHAR:
            $error = 'Unexpected control character found';
            break;
        case JSON_ERROR_SYNTAX:
            $error = 'Syntax error, malformed JSON';
            break;
        case JSON_ERROR_UTF8:
            $error = 'Malformed UTF-8 characters, possibly incorrectly encoded';
            break;
        default:
            $error = 'Unknown error decoding JSON';
            break;
    }

    die('Error decoding JSON: ' . $error);
}


$results = array_filter($data, function($item) use ($query) {
    $title = strtolower($item['title']);
    $content = strtolower($item['content']);

    $regex = implode('.*', str_split($query));
    return preg_match("/$regex/i", $title) || preg_match("/$regex/i", $content);
});

echo json_encode(array_values($results));

?>