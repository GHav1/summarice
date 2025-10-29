<?php
$conn = new mysqli("localhost", "root", "", "summarice_db");
$id = $_GET['id'];
$result = $conn->query("SELECT * FROM users WHERE id=$id");
$row = $result->fetch_assoc();

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $fullname = $_POST['fullname'];
    $password = password_hash($_POST['password'], PASSWORD_DEFAULT);
    $conn->query("UPDATE users SET full_name='$fullname', password='$password' WHERE id=$id");
    header("Location: manage_accounts.php");
}
?>
<!DOCTYPE html>
<html>
<head><title>Edit Account</title></head>
<body>
<h2>Edit Account</h2>
<form method="post">
    <label>Full Name:</label><br>
    <input type="text" name="fullname" value="<?= htmlspecialchars($row['full_name']) ?>" required><br><br>
    <label>New Password:</label><br>
    <input type="password" name="password" required><br><br>
    <button type="submit">Save</button>
</form>
</body>
</html>
