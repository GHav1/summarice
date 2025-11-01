<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

session_start();

// ✅ Restrict access to admin only
if (!isset($_SESSION['username']) || $_SESSION['username'] !== 'admin') {
    header("Location: loginpage.php");
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $book_name = trim($_POST['book_name'] ?? '');
    $author_name = trim($_POST['author_name'] ?? '');
    $content = trim($_POST['content'] ?? '');

    // ✅ Validate required fields
    if ($book_name === '' || $author_name === '' || $content === '') {
        header("Location: add_book.php?error=Missing+required+fields");
        exit;
    }

    // ✅ Prepare data for Python safely
    $encoded = http_build_query([
        "book_name"   => $book_name,
        "author_name" => $author_name,
        "content"     => $content
    ]);

    // ✅ Correct Python path (your verified working one)
    $python_path = "D:\\1oneoneone\\Files\\APPS 001\\schoolAppsDL\\Phyton 3\\python.exe";

    // ✅ Path to your Python script
    $script_path = "C:\\wamp64\\www\\summarice\\library\\book_library_add.py";

    // ✅ Properly escape the command for Windows
    $command = "\"$python_path\" \"$script_path\" " . escapeshellarg($encoded);

    // ✅ Execute and capture both stdout + stderr
    $output = shell_exec($command . " 2>&1");

    // ✅ Log the command and raw Python output (for debugging)
    file_put_contents(
        __DIR__ . "/debug_add_book.log",
        "-------------------------------\n" .
        "Timestamp: " . date("Y-m-d H:i:s") . "\n" .
        "Command:\n$command\n\n" .
        "Output:\n$output\n\n",
        FILE_APPEND
    );

    // ✅ Attempt to decode Python JSON response
    $response = json_decode(trim($output), true);

    if (is_array($response) && isset($response['status'])) {
        if ($response['status'] === 'success') {
            header("Location: add_book.php?success=1");
            exit;
        } elseif ($response['status'] === 'error') {
            $error = urlencode($response['message'] ?? 'Unknown error');
            $trace = urlencode($response['trace'] ?? '');
            header("Location: add_book.php?error=$error&trace=$trace");
            exit;
        }
    }

    // ⚠️ Fallback for non-JSON responses
    header("Location: add_book.php?error=Python+did+not+return+valid+JSON");
    exit;
}
?>
