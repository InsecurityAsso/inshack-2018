<?php
include 'db_fn.php';
// verify it's a post we're processing
if($_SERVER["REQUEST_METHOD"] != "POST") {
    header("Location: index.php");
    exit;
}

session_start();
// connect to db
$db_handle = connect_db('db', 'newuser', 'idontcare');

// check username
$safe_username = mysqli_real_escape_string($db_handle, $_POST['username']);
$sql = "SELECT * FROM users WHERE username='$safe_username'";
$result = mysqli_query($db_handle,$sql);

// if the number of results is not 1 row, wrong username so redirect
if(mysqli_num_rows($result) != 1) {
    sleep(3);
    header("Location: index.php");
    $_SESSION['erreur']=1;
    exit;
}

// if username exists, fetch row
$row = mysqli_fetch_array($result,MYSQLI_ASSOC);

// calculate hash with the input and the salt
$calc_hash = md5($_POST['password'].$row['pass_salt']);

// check against pw
if(!hash_equals($calc_hash,$row['pass_md5']) ) {
    sleep(3);
    header("Location: index.php");
    $_SESSION['erreur']=1;
    exit;
}

// if everything's ok, add the success field to the session of the user
$_SESSION['success'] = 1;

// free result set
mysqli_free_result($result);
// close the mysql connection
mysqli_close($db_handle);
?>
<!DOCTYPE HTML>
<html lang="en-US">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="0; url=emails.php">
        <script type="text/javascript">
            window.location.href = "emails.php"
        </script>
        <title>CrimeMail v13.37</title>
    </head>
    <body>
        Login successful!! If you are not redirected automatically, follow this <a href='emails.php'>link</a>.
    </body>
</html>
