<?php
	// Account details
	$apiKey = urlencode('GD0yaeOMrPI-J4cNCV2e5hXZNYigokItiezy4Ub4oR');
	
	// Inbox details
	$inbox_id = '808842';
 
	// Prepare data for POST request
	$data = 'apikey=' . $apiKey . '&inbox_id=' . $inbox_id;



 
	// Send the GET request with cURL
	$ch = curl_init('https://api.textlocal.in/get_messages/?' . $data);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	$response = curl_exec($ch);
	curl_close($ch);
	// $message=$_REQUEST['message'];
	//$result = json_decode($response,true);
	
	 
	 // echo "<pre>";
	  //print_r($result);
	 // echo "<pre>";
	  
	  
	  // echo $message;
	
	
	
	
	// Process your response here
	echo $response;
	
$file = 'data.json';
// Open the file to get existing content
$current = file_get_contents($file);
// Append a new person to the file
$current .= "$response";
// Write the contents back to the file
file_put_contents($file, $current);





?>
