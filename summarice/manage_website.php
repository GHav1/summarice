<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Website Management - Summarice</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        main {
            text-align: center;
            margin-top: 60px;
        }
        button {
            margin: 10px;
            padding: 12px 25px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        button:hover {
            background-color: #0056b3;
            transform: scale(1.05);
        }
    </style>
</head>
<body>

<header>
    <h1>Website Management</h1>
</header>

<main>
    <button onclick="location.href='add_book.php'">Add Book</button>
    <button onclick="location.href='book_library.php'">View Books</button>
    <br><br>
    <button onclick="location.href='admin_dashboard.php'">Back</button>
</main>

<footer>
    <p>&copy; 2025 Summarice Website</p>
</footer>

</body>
</html>

