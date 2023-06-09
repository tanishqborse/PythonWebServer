<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $name = $_POST['name'];
    $age = $_POST['age'];

    // Do any processing on the variables if needed

    // Echo the variables back to the client
    echo "Your name is: " . $name . "\n";
    echo "Your age is: " . $age . "\n";
}
?>
