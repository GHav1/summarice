<?php
session_start();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Summarice - Login</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>

<?php include 'header.php'; ?>

<main class="login-page">
    <section class="login-section">
        <h2>Login</h2>
        <p>Enter your credentials to continue.</p>

        <?php if (isset($_GET['error']) && $_GET['error'] === '1'): ?>
            <p class="error-message">❌ Incorrect username or password.</p>
        <?php elseif (isset($_GET['success']) && $_GET['success'] === '1'): ?>
            <p class="success-message">✅ Account created successfully. You can now log in!</p>
        <?php endif; ?>

        <form action="login.php" method="post" class="login-form">
            <label for="email">Username:</label>
            <input type="text" id="email" name="email" placeholder="Enter your username" required>

            <label for="password">Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <button type="submit">Login</button>

            <p class="signup-text">
                Don’t have an account? <a href="signup.php">Sign up</a>
            </p>
        </form>
    </section>
</main>

<footer>
    <p>&copy; 2025 Summarice Website</p>
</footer>

</body>
</html>
