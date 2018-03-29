<!DOCTYPE html>
<html lang="en"><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta author="yzoug">
    <link rel="icon" href="https://inshack.insecurity-insa.fr/img/favicon.ico" />

    <title>CrimeMail v13.37</title>

    <!-- Bootstrap core CSS -->
    <link href="bootstrap.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="signin.css" rel="stylesheet">
  </head>
  <body class="text-center">
    <form class="form-signin" action="auth.php" method="post">
      <img class="mb-4" src="logo.png" alt="" width="300">
      <!-- Credits to logomakr.com for the logo -->
      <h1 class="h3 mb-3 font-weight-normal">CrimeMail v13.37</h1>
      <p class="mb-3 font-weight-normal"> stylish email service for all your criminal needs </p>
<?php
session_start();
if (isset($_SESSION['erreur'])) {
    echo "<p class=\"font-weight-bold bg-danger\"> Invalid credentials </p>";
    unset($_SESSION['erreur']);
}
?>
      <label for="inputEmail" class="sr-only">Username</label>
      <input id="inputEmail" class="form-control" placeholder="Username" required="" autofocus="" data-cip-id="inputEmail" type="username" name="username">
      <label for="inputPassword" class="sr-only">Password</label>
      <input id="inputPassword" class="form-control" placeholder="Password" required="" data-cip-id="inputPassword" type="password" name="password">
      <div class="checkbox mb-3">
        <label>
          <input value="remember-me" type="checkbox" required> I am not trying to hack this
        </label>
      </div>
      <hr>
      <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
      <p class="mt-5 mb-3 text-muted">© INSHACK 2017-2018. <a href="forgot.php">Lost password?</a></p>
    </form>
  </body>
</html>
