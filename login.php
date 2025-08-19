<?php
session_start();
require 'dbconnect.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST['email'];
    $password = $_POST['password'];

    $result = $conn->query("SELECT * FROM users WHERE email='$email'");
    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        if ($password === $row['password']) {   // direct comparison
            $_SESSION['email'] = $email;
            echo "Welcome, " . $email . "! You are logged in. <a href='logout.php'>Logout</a>";
        } else {
            echo "Incorrect password. <a href='green.php'>Try again</a>";
        }
    } else {
        echo "No account found with this email. <a href='green.php'>Sign up</a>";
    }
}
?>

