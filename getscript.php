<?php

if (isset($_GET['name']) && isset($_GET['age'])) {
  $name = $_GET['name'];
  $age = $_GET['age'];
  echo "Hello $name, you are $age years old.";
}

?>