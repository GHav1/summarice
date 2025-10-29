<?php
$book_name = $_POST['book_name'];
$author_name = $_POST['author_name'];
$content = $_POST['content'];

// Escape input for safety
$book_name = escapeshellarg($book_name);
$author_name = escapeshellarg($author_name);
$content = escapeshellarg($content);

// Run the Python script
$command = "python ./library/book_library_add.py $book_name $author_name $content";
$output = shell_exec($command);

echo "<h2>$output</h2>";
echo "<a href='add_book.php'>Back</a>";
?>
