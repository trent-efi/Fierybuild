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
        //$line = str_replace('','',$line);
	$temp = array();
        $first = 0;
        $max = count($line);
	for($i = 0; $i < $max; $i++){
	    if($first == 0){
	        $first = 1;
	        $temp[] = $line[$i];
	    } else {
	        $temp[] = intval($line[$i]);	        
	    }
	    //echo "";
	}

        //$data[] = $line;
        $data[] = $temp;
    }

    fclose($file);
    return json_encode($data);
}
?>
