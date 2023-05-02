<?php
header('Content-Type: application/json');

$query = $_GET['query'] ?? '';
$query = strtolower(trim($query));

if (strlen($query) < 3) {
    echo json_encode([]);
    exit;
}

$data = [];
$results = [];

if (file_exists('website_data.json')) {
    $data = json_decode(file_get_contents('website_data.json'), true);
}

foreach ($data as $item) {
    $title = strtolower($item['title']);
    $content = strtolower($item['content']);

    if (strpos($title, $query) !== false || strpos($content, $query) !== false) {
        $results[] = $item;
    }
}

echo json_encode($results);
?>
