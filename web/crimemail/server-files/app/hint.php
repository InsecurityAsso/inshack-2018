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
          <div class="jumbotron horizontal-center">
            <p> Here is the requested hint for this username: </p>
<b>
<pre>
<?php

include 'db_fn.php';
// redirect if it's not an http post
if($_SERVER["REQUEST_METHOD"] != "POST") {
    header("Location: forgot.php");
    exit;
}

// connect to db
// WE NEED TO USE A SPECIAL USER WITH READ ONLY ACCESS
$db_handle = connect_db('db', 'newuser', 'idontcare');
// for mysql/mariadb:
// CREATE USER 'anonymous'@'%';
// GRANT SELECT ON db.* TO 'anonymous'@'%';

// EXPLOIT: possible sql injection
$username = $_POST["username"];
$sql = "SELECT hint FROM users WHERE username='$username'";

$pos1 = stripos($sql, 'sleep');
$pos2 = stripos($sql, 'benchmark');
//$pos3 = stripos($sql, '');

if ($pos1 !== false or $pos2 !== false) {
    $sql = "select 'Please don\'t try to destroy the chall!!' AS ''";
}

// get the result or results
$result = mysqli_query($db_handle,$sql);

// error handling (and showing to people)
if (!$result) {
    die('Database error: '.$db_handle->error);
    exit;
}

// error message if username doesn't exist
if ($result->num_rows === 0) {
    echo "We could not find the specified username. Are you sure you have an account with us?";
    exit;
}

// display the results (the hint associated with the username... or random stuff)
$hint = mysqli_fetch_all($result, MYSQLI_ASSOC);
var_dump($hint);

while($row = $result->fetch_row()) {
  $rows[]=$row;
}

foreach ($row as &$rows) {
    echo $row;
}

// free result set
mysqli_free_result($result);
// close the mysql connection
mysqli_close($db_handle);
//*/
?>
</pre>
</b>
          </div>
      </div>
      <p class="mt-5 mb-3 text-muted">© INSHACK 2017-2018. <a href="index.php">Go back to sign-in</a></p>
  </body>
</html>
