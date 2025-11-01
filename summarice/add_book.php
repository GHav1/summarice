<?php
session_start();

// Restrict access to admin only
if (!isset($_SESSION['username']) || $_SESSION['username'] !== 'admin') {
    header("Location: loginpage.php");
    exit;
}

include 'header.php';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Book - Summarice</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        .add-book-container {
            max-width: 600px;
            margin: 40px auto;
            background: #fff;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .add-book-container h2 {
            text-align: center;
            color: #333;
            margin-bottom: 20px;
        }
        .input-row {
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
        }
        label {
            font-weight: bold;
            color: #333;
        }
        input, textarea {
            width: 100%;
            padding: 10px;
            border-radius: 6px;
            border: 1px solid #ccc;
        }
        button {
            display: block;
            width: 100%;
            background-color: #28a745;
            color: white;
            border: none;
            padding: 10px 0;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 15px;
        }
        button:hover {
            background-color: #218838;
        }
        .back-btn {
            background-color: #6c757d;
        }
        .back-btn:hover {
            background-color: #5a6268;
        }
        .success-message {
            text-align: center;
            color: green;
            font-weight: bold;
        }
        .error-message {
            text-align: center;
            color: red;
            font-weight: bold;
        }
    </style>
</head>
<body>

<main>
    <div class="add-book-container">
        <h2>Add a New Book</h2>

        <?php if (isset($_GET['success']) && $_GET['success'] == 1): ?>
            <p class="success-message">✅ Book added successfully!</p>
        <?php elseif (isset($_GET['error'])): ?>
            <p class="error-message">❌ Error adding book: <?php echo htmlspecialchars($_GET['error']); ?></p>
        <?php endif; ?>

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

        <button class="back-btn" onclick="location.href='manage_website.php'">Back</button>
    </div>
</main>

<footer>
    <p>&copy; 2025 Summarice Website</p>
</footer>

</body>
</html>
