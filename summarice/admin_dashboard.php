<?php
session_start();
if (!isset($_SESSION['username']) || $_SESSION['username'] !== 'admin') {
    header("Location: loginpage.php");
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        main {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            min-height: 70vh;
            gap: 20px;
        }
        .admin-btn {
            padding: 15px 30px;
            font-size: 18px;
            cursor: pointer;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
        }
        .admin-btn:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <header>
        <h1>Admin Dashboard</h1>
        <p>Welcome, Administrator!</p>
    </header>

    <main>
        <button class="admin-btn" onclick="location.href='manage_accounts.php'">Accounts</button>
        <button class="admin-btn" onclick="location.href='manage_website.php'">Website</button>
        <button class="admin-btn" onclick="location.href='manage_requests.php'">Request</button>
    </main>
</body>
</html>
