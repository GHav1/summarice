<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
?>
<header>
    <h1>Welcome to Summarice</h1>
    <p>Simple Summary Library</p>
</header>

<nav class="navbar">
    <div class="nav-left">
        <a href="index.php">Home</a>
        <a href="about.php">About</a>

        <?php if (isset($_SESSION['username'])): ?>
            <?php if ($_SESSION['role'] === 'admin'): ?>
                <a href="admin_dashboard.php">Dashboard</a>
                <a href="book_library.php">Library</a>
            <?php else: ?>
                <a href="book_library.php">Library</a>
                <a href="manage_requests.php">Request</a>
            <?php endif; ?>
        <?php endif; ?>
    </div>

    <div class="nav-right">
        <?php if (isset($_SESSION['username'])): ?>
            <span class="username">👤 <?php echo htmlspecialchars($_SESSION['username']); ?></span>
            <a href="logout.php" class="logout-btn">Logout</a>
        <?php else: ?>
            <a href="loginpage.php">Login</a>
            <a href="signup.php">Sign Up</a>
        <?php endif; ?>
    </div>
</nav>

<style>
    /* --- Make header fixed --- */
    header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 1000;
        background-color: #f8f8f8; /* Adjusted to make header stand out more */
        padding: 10px 20px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    }

    header h1, header p {
        margin: 0;
        padding: 0;
        color: #333;
    }

    .navbar {
        position: fixed;
        top: 100px; /* Adjust depending on your header height */
        left: 0;
        width: 100%;
        background-color: #222;
        color: white;
        z-index: 999;
        padding: 10px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    }

    .nav-left a, .nav-right a {
        color: white;
        text-decoration: none;
        padding: 10px 15px;
        display: inline-block;
    }

    .nav-left a:hover, .nav-right a:hover {
        background-color: #444;
    }

    .nav-right .username {
        margin-right: 15px;
        font-weight: bold;
    }

    .nav-right .logout-btn {
        background-color: #e74c3c;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        text-decoration: none;
    }

    /* --- Prevent content from hiding under fixed header --- */
    body {
        margin: 0;
        padding-top: calc(100px + 50px); /* Adjust to match your header + navbar height */
        font-family: Arial, sans-serif;
        box-sizing: border-box;
    }
</style>