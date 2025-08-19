<?php session_start(); ?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Greenwish</title>
  <link rel="stylesheet" href="wish.css"/>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
  <style>
    /* Logo styling */
    .logo {
      width: 120px;
      height: auto;
      display: block;
      margin: 0 auto 20px;
    }

    /* Center text for title under logo */
    .title {
      text-align: center;
      font-size: 1.5rem;
      margin-bottom: 20px;
    }

    /* Center the welcome text */
    #welcome-screen h1, #welcome-screen h2 {
      text-align: center;
    }

    /* Buttons styling if needed */
    .main-btn, .alt-btn {
      display: block;
      margin: 10px auto;
      padding: 10px 20px;
      font-size: 1rem;
      cursor: pointer;
    }
  </style>
</head>
<body>

  <!-- Welcome Screen -->
  <div id="welcome-screen" class="screen">
    <div class="background-shape"></div>
    <h2>Welcome to</h2>
    <img src="logo.png" alt="Greenwish Logo" class="logo">
    <h1>Greenwish</h1>
    <button class="main-btn" onclick="showSignup()">Get started <span class="arrow">➜</span></button>
  </div>

  <!-- Signup Screen -->
  <div id="signup-screen" class="screen hidden">
   <div class="logo-wrapper">
  <img src="logo.png" alt="Greenwish Logo" class="logo">
</div>
    <!--hello-->
    <p class="title">Create an account</p>

    <form action="signup.php" method="POST">
      <div>
        <input type="email" name="email" placeholder="email@domain.com" required />
      </div>
      <div>
        <input type="password" name="password" placeholder="Password" required />
      </div>
      <div>
        <button type="submit" class="main-btn">Sign Up</button>
      </div>
    </form>

    <p class="alt-text" style="text-align:center;">Already have an account?</p>
    <button class="alt-btn" onclick="showLogin()">Login</button>
  </div>

  <!-- Login Screen -->
  <div id="login-screen" class="screen hidden">
    <img src="logo.png" alt="Greenwish Logo" class="logo">
    <p class="title">Login</p>

    <form action="login.php" method="POST">
      <div>
        <input type="email" name="email" placeholder="email@domain.com" required />
      </div>
      <div>
        <input type="password" name="password" placeholder="Password" required />
      </div>
      <div>
        <button type="submit" class="main-btn">Login</button>
      </div>
    </form>

    <p class="alt-text" style="text-align:center;">Don't have an account?</p>
    <button class="alt-btn" onclick="showSignup()">Sign Up</button>
  </div>

  <script src="green.js"></script>
</body>
</html>
