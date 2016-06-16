<?php
$action = $_POST['function'];

switch($action) {
    case 'read_csv': $csv = $_POST['csv']; echo read_csv($csv); break;
    default: break;
}

function read_csv($csv){
    $file_path = "csv/".$csv;
    $file = fopen($file_path,"r");
    $data = array();
    
    //$data = fgetcsv($file);
    while( ($line = fgetcsv($file)) !== false) {
        $data[] = $line;
    }

    fclose($file);
    return json_encode($data);
}
?>
