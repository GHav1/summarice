<?php
session_start();

// Database connection
$servername = "localhost";
$dbusername = "root";
$dbpassword = "";
$dbname = "summarice_db";

$conn = new mysqli($servername, $dbusername, $dbpassword, $dbname);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Collect form input
$user = trim($_POST['email']); //
$pass = trim($_POST['password']);

if (empty($user) || empty($pass)) {
    header("Location: loginpage.php?error=1");
    exit;
}

// check username 
$sql = "SELECT * FROM users WHERE username = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $user);
$stmt->execute();
$result = $stmt->get_result();

if ($result && $result->num_rows > 0) {
    $row = $result->fetch_assoc();

    if (password_verify($pass, $row['password'])) {
        $_SESSION['username'] = $row['username'];
        $_SESSION['fullname'] = $row['full_name'] ?? $row['username'];
        $_SESSION['role'] = $row['role'] ?? 'user';

        if ($_SESSION['role'] === 'admin') {
            header("Location: admin_dashboard.php");
        } else {
            header("Location: index.php");
        }
        exit;
    } else {
        header("Location: loginpage.php?error=1");
        exit;
    }
} else {
    header("Location: loginpage.php?error=1");
    exit;
}

$stmt->close();
$conn->close();
