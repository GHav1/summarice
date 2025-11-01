<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
?>
<header class="site-header">
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
            <a href="signup.php" class="signup-btn">Sign Up</a>
        <?php endif; ?>
    </div>
</nav>

<style>
/* ---------- Header ---------- */
.site-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background-color: #4CAF50;
    color: white;
    text-align: center;
    padding: 18px 20px 12px 20px; /* slightly taller for balance */
    margin: 0;
    z-index: 1000;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.site-header h1,
.site-header p {
    margin: 0;
}

/* ---------- Navigation Bar ---------- */
.navbar {
    position: fixed;
    top: 95px; /* directly below header */
    left: 0;
    width: 100%;
    background-color: #222;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 25px; /* increased height to prevent cropping */
    z-index: 999;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.nav-left,
.nav-right {
    display: flex;
    align-items: center;
    flex-wrap: wrap; /* ensures no cropping if content is wide */
}

.nav-left a,
.nav-right a {
    color: white;
    text-decoration: none;
    padding: 10px 16px;
    font-weight: bold;
    border-radius: 4px;
    transition: background-color 0.3s ease;
    white-space: nowrap;
}

.nav-left a:hover,
.nav-right a:hover {
    background-color: #4CAF50;
}

.username {
    margin-right: 15px;
    font-weight: bold;
    color: #ddd;
}

.logout-btn {
    background-color: #e74c3c;
    color: white;
    padding: 8px 16px;
    border-radius: 5px;
    text-decoration: none;
    font-weight: bold;
    transition: background-color 0.3s ease;
}

.logout-btn:hover {
    background-color: #c0392b;
}

.signup-btn {
    background-color: #4CAF50;
    color: white;
    padding: 8px 16px;
    border-radius: 5px;
    text-decoration: none;
    font-weight: bold;
}

.signup-btn:hover {
    background-color: #45a049;
}

/* ---------- Body Padding Fix ---------- */
body {
    margin: 0;
    padding-top: 185px; /* enough for header (95) + navbar (90) */
    background-color: #f4f4f4;
    font-family: Arial, sans-serif;
}
</style>
