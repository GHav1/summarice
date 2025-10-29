<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "summarice_db";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error);

$user = $_POST['email'];
$pass = $_POST['password'];

$sql = "SELECT * FROM users WHERE username = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $user);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();

    if (password_verify($pass, $row['password'])) {
        session_start();
        $_SESSION['username'] = $row['username'];
        $_SESSION['fullname'] = $row['full_name'];

        if ($row['username'] === 'admin') {
            header("Location: admin_dashboard.php");
        } else {
            echo "Welcome, " . htmlspecialchars($row['full_name']) . "! (You are logged in.)";
        }
        exit;
    } else {
        echo "Invalid password.";
    }
} else {
    echo "User not found.";
}

$stmt->close();
$conn->close();
?>