<?php
session_start();

// Redir if no admi
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
    <title>Admin Dashboard - Summarice</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        .dashboard {
            text-align: center;
            margin-top: 40px;
        }

        .dashboard h2 {
            font-size: 2em;
            margin-bottom: 20px;
        }

        .button-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            margin-top: 30px;
        }

        .dashboard-button {
            background-color: #007bff;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }

        .dashboard-button:hover {
            background-color: #0056b3;
            transform: scale(1.05);
        }

        footer {
            text-align: center;
            margin-top: 50px;
            color: #666;
        }
    </style>
</head>
<body>
    <main>
        <section class="dashboard">
            <h2>Welcome, <?php echo htmlspecialchars($_SESSION['fullname']); ?>!</h2>
            <p>Manage the system:</p>

            <div class="button-container">
                <form action="manage_accounts.php" method="get">
                    <button class="dashboard-button" type="submit">Accounts</button>
                </form>

                <form action="manage_website.php" method="get">
                    <button class="dashboard-button" type="submit">Website</button>
                </form>

                <form action="manage_requests.php" method="get">
                    <button class="dashboard-button" type="submit">Requests</button>
                </form>
            </div>
        </section>
    </main>

    <footer>
        <p>&copy; 2025 Summarice Website</p>
    </footer>
</body>
</html>
