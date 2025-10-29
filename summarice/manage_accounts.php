<?php
session_start();
if (!isset($_SESSION['username']) || $_SESSION['username'] !== 'admin') {
    header("Location: loginpage.html");
    exit;
}

$conn = new mysqli("localhost", "root", "", "summarice_db");

if (isset($_GET['delete'])) {
    $id = $_GET['delete'];
    $conn->query("DELETE FROM users WHERE id=$id");
}

$result = $conn->query("SELECT * FROM users");
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Manage Accounts</title>
<link rel="stylesheet" href="styles.css">
</head>
<body>
<header><h1>Manage Accounts</h1></header>
<main>
<table border="1" cellpadding="10">
<tr><th>ID</th><th>Full Name</th><th>Username</th><th>Actions</th></tr>
<?php while ($row = $result->fetch_assoc()): ?>
<tr>
    <td><?= $row['id'] ?></td>
    <td><?= htmlspecialchars($row['full_name']) ?></td>
    <td><?= htmlspecialchars($row['username']) ?></td>
    <td>
        <a href="edit_account.php?id=<?= $row['id'] ?>">Edit</a> |
        <a href="?delete=<?= $row['id'] ?>" onclick="return confirm('Delete this account?')">Delete</a>
    </td>
</tr>
<?php endwhile; ?>
</table>
<br>
<button onclick="location.href='admin_dashboard.php'">Back</button>
</main>
</body>
</html>
