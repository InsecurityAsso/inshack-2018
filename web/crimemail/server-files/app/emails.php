<?php
session_start();
if(!isset($_SESSION['success'])) {
    header("Location: index.php");
    exit;
}
unset($_SESSION['success']);
?>
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
    <link href="forgot.css" rel="stylesheet">
  </head>

  <body class="text-center">
      <div class="container">
            <img src="logo.png" width="300" alt="">
            <!-- Credits to logomakr.com for the logo -->
            <hr>
            <p class="text-left"> Welcome to CrimeMail! Here is the last received messages:</p>
          <div class="jumbotron horizontal-center">
              <p class="text-weight-bold text-left"> UNKNOWN SENDER says: </p>
              <p class="text-weight-normal text-center"> Meet me at INSA{s3cr3t_l0cat10n} </p>
         </div>
      </div>
      <p class="mt-5 mb-3 text-muted">© INSHACK 2017-2018. <a href="index.php">Go back to sign-in</a></p>
    </form>
  </body>
</html>
