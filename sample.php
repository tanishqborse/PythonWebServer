<?php

// Get the value of the "name" and "age" parameters from the query string
$name = $_GET['name'];
$age = $_GET['age'];

// Print out a message containing the values of the "name" and "age" parameters
echo "Hello, $name! You are $age years old.";

?>