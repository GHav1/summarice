<?php
session_start();
include 'header.php';
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Summarice - Sign Up</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>

<main class="signup-page">
    <section class="signup-section">
        <h2>Create Your Summarice Account</h2>
        <p>Fill in the details below to create your account.</p>

        <form action="register.php" method="post" class="signup-form">
            <label for="fullname">Full Name:</label><br>
            <input type="text" id="fullname" name="fullname" placeholder="Enter your full name" required><br><br>

            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username" placeholder="Enter a username" required><br><br>

            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password" placeholder="Enter your password" required><br><br>

            <label for="confirm">Confirm Password:</label><br>
            <input type="password" id="confirm" name="confirm" placeholder="Re-enter your password" required><br><br>

            <button type="submit">Register</button>

            <p class="login-text">
                Already have an account? <a href="loginpage.php">Login here</a>
            </p>
        </form>
    </section>
</main>

<footer>
    <p>&copy; 2025 Summarice Website</p>
</footer>

</body>
</html>
