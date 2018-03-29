<?php
function connect_db($database, $db_user, $db_password, $host = 'localhost', $die = true) {
	// Returns a MySQL link identifier (handle) on success
	// Returns false or dies() on error depending on the setting of parameter $die
	// Parameter $die configures error handling, setting it any non-false value will die() on error
	// Parameters $host, $port and $die have sensible defaults and are not usually required

	if(!$db_handle = mysqli_connect($host, $db_user, $db_password, $database)) {
		if($die)
			die("Can't connect to MySQL server or database:\r\n".mysql_error());
		else
			return false;
	}
/*	if(!@mysqli_select_db($database, $db_handle)) {
		if($die)
			die("Can't select database '$database':\r\n".mysql_error());
		else
			return false;
    }*/
	return $db_handle;
}
?>
