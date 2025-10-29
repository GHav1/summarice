<?php
$servername = "localhost";
$username = "root"; // default for WAMP
$password = ""; // leave blank unless you set one
$dbname = "summarice_db";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$fullname = $_POST['fullname'];
$user = $_POST['username'];
$pass = $_POST['password'];
$confirm = $_POST['confirm'];

if ($pass !== $confirm) {
    die("Passwords do not match! <a href='signup.html'>Try again</a>");
}

$hashedPassword = password_hash($pass, PASSWORD_DEFAULT);

$sql = "INSERT INTO users (full_name, username, password) VALUES (?, ?, ?)";
$stmt = $conn->prepare($sql);
$stmt->bind_param("sss", $fullname, $user, $hashedPassword);

if ($stmt->execute()) {
    echo "Registration successful! <a href='loginpage.html'>Login now</a>";
} else {
    echo "Error: " . $stmt->error;
}

$stmt->close();
$conn->close();
?>
