<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);
session_start();

include 'header.php';

// ✅ Python setup
$python_path = "D:\\1oneoneone\\Files\\APPS 001\\schoolAppsDL\\Phyton 3\\python.exe";
$script_path = "C:\\wamp64\\www\\summarice\\library\\book_library.py";
$command = "\"$python_path\" \"$script_path\"";

$output = shell_exec($command . " 2>&1");

// ✅ Log any unexpected issues
file_put_contents(
    __DIR__ . "/debug_library.log",
    "Command:\n$command\n\nOutput:\n$output\n\n",
    FILE_APPEND
);

$books = json_decode($output, true);
if (!is_array($books)) {
    $books = [];
}

// ✅ Search logic
$search = isset($_GET['search']) ? strtolower(trim($_GET['search'])) : '';
$filtered_books = [];

foreach ($books as $book) {
    if (
        !$search ||
        (isset($book['title']) && strpos(strtolower($book['title']), $search) !== false) ||
        (isset($book['author']) && strpos(strtolower($book['author']), $search) !== false)
    ) {
        $filtered_books[] = $book;
    }
}

// ✅ Pagination setup
$books_per_page = 3;
$total_books = count($filtered_books);
$total_pages = ceil($total_books / $books_per_page);
$current_page = isset($_GET['page'])
    ? max(1, min((int)$_GET['page'], $total_pages))
    : 1;

$start_index = ($current_page - 1) * $books_per_page;
$paginated_books = array_slice($filtered_books, $start_index, $books_per_page);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Library - Summarice</title>
    <link rel="stylesheet" href="styles.css">

    <style>
        main {
            padding-top: 40px;
            padding-bottom: 120px; /* Prevent overlap with fixed footer */
            max-width: 900px;
            margin: 0 auto;
        }

        /* Search bar styling */
        .search-container {
            text-align: center;
            margin-bottom: 30px;
            margin-top: 20px;
        }

        .search-container form {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
        }

        .search-container input[type="text"] {
            width: 60%;
            max-width: 400px;
            padding: 10px;
            border-radius: 6px;
            border: 1px solid #ccc;
            font-size: 16px;
        }

        .search-container button {
            padding: 10px 15px;
            border: none;
            background: #4CAF50;
            color: white;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .search-container button:hover {
            background: #45a049;
        }

        /* Book card layout */
        .book-list {
            display: flex;
            flex-direction: column;
            gap: 25px;
            margin-bottom: 100px;
        }

        .book-item {
            background: white;
            border-radius: 10px;
            padding: 20px 25px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            word-wrap: break-word;
            text-align: left;
        }

        .book-item strong {
            font-size: 1.3em;
            color: #222;
        }

        .book-item em {
            color: #555;
        }

        .book-item p {
            color: #333;
            line-height: 1.6;
            margin-top: 12px;
            white-space: pre-wrap;
        }

        /* Pagination controls */
        .pagination {
            text-align: center;
            margin-top: 30px;
        }

        .pagination a,
        .pagination span {
            display: inline-block;
            padding: 10px 15px;
            border-radius: 5px;
            margin: 0 5px;
            text-decoration: none;
            color: white;
            background: #4CAF50;
        }

        .pagination a:hover {
            background: #45a049;
        }

        .pagination .disabled {
            background: #aaa;
            pointer-events: none;
        }
    </style>
</head>

<body>
    <main>
        <section class="library-section">
            <h2 style="text-align:center;">📚 Library</h2>

            <!-- Search Bar -->
            <div class="search-container">
                <form method="get">
                    <input
                        type="text"
                        name="search"
                        placeholder="Search a book..."
                        value="<?php echo htmlspecialchars($search); ?>"
                    >
                    <button type="submit">Search</button>
                </form>
            </div>

            <!-- Book List -->
            <div class="book-list">
                <?php if (empty($paginated_books)): ?>
                    <p style="color:red;text-align:center;">No books found in the library.</p>
                <?php else: ?>
                    <?php foreach ($paginated_books as $book): ?>
                        <div class="book-item">
                            <strong><?php echo htmlspecialchars($book['title']); ?></strong><br>
                            <em>by <?php echo htmlspecialchars($book['author']); ?></em><br><br>
                            <p><?php echo nl2br(htmlspecialchars($book['content'] ?? '')); ?></p>
                        </div>
                    <?php endforeach; ?>
                <?php endif; ?>
            </div>

            <!-- Pagination -->
            <div class="pagination">
                <?php if ($current_page > 1): ?>
                    <a href="?page=<?php echo $current_page - 1; ?>&search=<?php echo urlencode($search); ?>">Previous</a>
                <?php else: ?>
                    <span class="disabled">Previous</span>
                <?php endif; ?>

                <?php if ($current_page < $total_pages): ?>
                    <a href="?page=<?php echo $current_page + 1; ?>&search=<?php echo urlencode($search); ?>">Next</a>
                <?php else: ?>
                    <span class="disabled">Next</span>
                <?php endif; ?>
            </div>
        </section>
    </main>

    <footer>
        <p>&copy; 2025 Summarice Website</p>
    </footer>
</body>
</html>
