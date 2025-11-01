old book_library.php

<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

session_start();
include 'header.php';

// ✅ Everyone can view

$python_path = "D:\\1oneoneone\\Files\\APPS 001\\schoolAppsDL\\Phyton 3\\python.exe";
$script_path = "C:\\wamp64\\www\\summarice\\library\\book_library.py";

$command = "\"$python_path\" \"$script_path\"";
$output = shell_exec($command . " 2>&1");

// Debug log
file_put_contents(__DIR__ . "/debug_library.log", "Command:\n$command\n\nOutput:\n$output\n\n", FILE_APPEND);

$books = json_decode($output, true);
if (!is_array($books)) {
    $books = [];
}

// ✅ Search filter
$search = isset($_GET['search']) ? strtolower(trim($_GET['search'])) : '';
$filtered_books = [];

if ($search) {
    foreach ($books as $book) {
        if (
            (isset($book['title']) && strpos(strtolower($book['title']), $search) !== false) ||
            (isset($book['author']) && strpos(strtolower($book['author']), $search) !== false)
        ) {
            $filtered_books[] = $book;
        }
    }
} else {
    $filtered_books = $books;
}

// ✅ Pagination setup
$books_per_page = 3;
$total_books = count($filtered_books);
$total_pages = max(1, ceil($total_books / $books_per_page));
$current_page = isset($_GET['page']) ? max(1, intval($_GET['page'])) : 1;
if ($current_page > $total_pages) $current_page = $total_pages;
$start_index = ($current_page - 1) * $books_per_page;
$display_books = array_slice($filtered_books, $start_index, $books_per_page);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Library - Summarice</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        body {
            background-color: #f2f2f2;
            font-family: Arial, sans-serif;
        }
        main {
            margin-top: 160px; /* ✅ pushes below fixed header/navigation */
        }
        .library-header {
            text-align: center;
            margin-bottom: 25px;
        }
        .library-header h2 {
            font-size: 2em;
            color: #333;
            margin-bottom: 10px;
        }
        .search-container {
            text-align: center;
            margin-bottom: 30px;
        }
        .search-container input {
            width: 250px;
            padding: 8px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        .search-container button {
            padding: 8px 14px;
            border: none;
            background: #28a745;
            color: #fff;
            border-radius: 5px;
            cursor: pointer;
        }
        .search-container button:hover {
            background: #218838;
        }
        .book-item {
            margin: 20px auto;
            padding: 20px;
            max-width: 700px;
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 3px 8px rgba(0,0,0,0.1);
        }
        .book-item strong {
            font-size: 1.2em;
            color: #333;
        }
        .book-item em {
            color: #666;
        }
        .pagination {
            text-align: center;
            margin: 40px 0;
        }
        .pagination a, .pagination span {
            display: inline-block;
            padding: 10px 16px;
            margin: 0 5px;
            border-radius: 8px;
            font-weight: bold;
            text-decoration: none;
            transition: all 0.2s ease-in-out;
        }
        .pagination a {
            background: #28a745;
            color: white;
            border: 1px solid #1e7e34;
        }
        .pagination a:hover {
            background: #218838;
        }
        .pagination span {
            background: #333;
            color: #fff;
            border: 1px solid #111;
        }
    </style>
</head>
<body>

<main>
    <section class="library-section">

        <!-- ✅ Now properly placed below navigation -->
        <div class="library-header">
            <h2>📚 Library</h2>
            <p>Simple Summarice Library</p>
        </div>

        <div class="search-container">
            <form method="get">
                <input type="text" name="search" placeholder="Search a book..."
                       value="<?php echo htmlspecialchars($search); ?>">
                <button type="submit">Search</button>
            </form>
        </div>

        <div class="book-list">
            <?php if (empty($display_books)): ?>
                <p style="color:red;text-align:center;">No books found in the library.</p>
            <?php else: ?>
                <?php foreach ($display_books as $book): ?>
                    <div class="book-item">
                        <strong><?php echo htmlspecialchars($book['title'] ?? 'Untitled'); ?></strong><br>
                        <em>by <?php echo htmlspecialchars($book['author'] ?? 'Unknown'); ?></em><br><br>
                        <p><?php echo nl2br(htmlspecialchars($book['content'] ?? 'No content available.')); ?></p>
                    </div>
                <?php endforeach; ?>
            <?php endif; ?>
        </div>

        <?php if ($total_pages > 1): ?>
        <div class="pagination">
            <?php if ($current_page > 1): ?>
                <a href="?<?php echo http_build_query(['page' => $current_page - 1, 'search' => $search]); ?>">⬅ Previous</a>
            <?php endif; ?>
            <span>Page <?php echo $current_page; ?> of <?php echo $total_pages; ?></span>
            <?php if ($current_page < $total_pages): ?>
                <a href="?<?php echo http_build_query(['page' => $current_page + 1, 'search' => $search]); ?>">Next ➡</a>
            <?php endif; ?>
        </div>
        <?php endif; ?>

    </section>
</main>

<footer>
    <p>&copy; 2025 Summarice Website</p>
</footer>

</body>
</html>