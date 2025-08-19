<?php
session_start();
require 'dbconnect.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST['email'];
    $password = $_POST['password'];

    // Check if email already exists
    $check = $conn->query("SELECT * FROM users WHERE email='$email'");
    if ($check->num_rows > 0) {
        echo "Email already registered. <a href='green.php'>Try again</a>";
    } else {
        $sql = "INSERT INTO users (email, password) VALUES ('$email', '$password')";
        if ($conn->query($sql) === TRUE) {
            echo "Account created successfully! <a href='green.php'>Login now</a>";
        } else {
            echo "Error: " . $conn->error;
        }
    }
}
?>

