<?php
session_start();
if (!isset($_SESSION['username']) || $_SESSION['username'] !== 'admin') {
    header("Location: loginpage.html");
    exit;
}
?>
<!DOCTYPE html>
<html>
<head>
<title>Add Book</title>
<link rel="stylesheet" href="styles.css">
<style>
    .add-book-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
        width: 500px;
        margin: auto;
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    .input-row {
        display: flex;
        justify-content: space-between;
        gap: 10px;
    }
    input, textarea {
        width: 100%;
        padding: 10px;
    }
</style>
</head>
<body>
<header><h1>Add a New Book</h1></header>
<main>
<div class="add-book-container">
<form action="add_book_process.php" method="post">
    <div class="input-row">
        <div style="flex:1;">
            <label>Book Name:</label><br>
            <input type="text" name="book_name" required>
        </div>
        <div style="flex:1;">
            <label>Author Name:</label><br>
            <input type="text" name="author_name" required>
        </div>
    </div>
    <label>Book Content:</label><br>
    <textarea name="content" rows="6" required></textarea>
    <button type="submit">Add Book</button>
</form>
<br>
<button onclick="location.href='manage_website.php'">Back</button>
</div>
</main>
</body>
</html>
