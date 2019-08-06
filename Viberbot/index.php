<?php 

$auth_token = "AUTH_TOKEN";
$send_name = "HelloBot";
$is_log = true;

function put_log_in($data)
{
	global $is_log;
	if($is_log) {file_put_contents("tmp_in.txt", $data."\n", FILE_APPEND);}
}

function put_log_out($data)
{
	global $is_log;
	if($is_log) {file_put_contents("tmp_out.txt", $data."\n", FILE_APPEND);}
}

function sendReq($data)
{
	$request_data = json_encode($data);
	put_log_out($request_data);
	
	//here goes the curl to send data to user
	$ch = curl_init("https://chatapi.viber.com/pa/send_message");
	curl_setopt($ch, CURLOPT_POST, 1);
	curl_setopt($ch, CURLOPT_POSTFIELDS, $request_data);
	curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
	$response = curl_exec($ch);
	$err = curl_error($ch);
	curl_close($ch);
	if($err) {return $err;}
	else {return $response;}
}

function sendMsg($sender_id, $text, $type, $tracking_data = Null, $arr_asoc = Null)
{
	global $auth_token, $send_name;
  
	$data['auth_token'] = $auth_token;
	$data['receiver'] = $sender_id;
	if($text != Null) {$data['text'] = $text;}
	$data['type'] = $type;
	//$data['min_api_version'] = $input['sender']['api_version'];
	$data['sender']['name'] = $send_name;
	//$data['sender']['avatar'] = $input['sender']['avatar'];
	if($tracking_data != Null) {$data['tracking_data'] = $tracking_data;}
	if($arr_asoc != Null)
	{
		foreach($arr_asoc as $key => $val) {$data[$key] = $val;}
	}
	
	return sendReq($data);
}

function sendMsgText($sender_id, $text, $tracking_data = Null)
{
	return sendMsg($sender_id, $text, "text", $tracking_data);
}

$request = file_get_contents("php://input");
$input = json_decode($request, true);
put_log_in($request);

$type = $input['message']['type']; //type of message received (text/picture)
$text = $input['message']['text']; //actual message the user has sent
$sender_id = $input['sender']['id']; //unique viber id of user who sent the message
$sender_name = $input['sender']['name']; //name of the user who sent the message

if($input['event'] == 'webhook') 
{
  $webhook_response['status'] = 0;
  $webhook_response['status_message'] = "ok";
  $webhook_response['event_types'] = 'delivered';
  echo json_encode($webhook_response);
  die;
}
else if($input['event'] == "subscribed") 
{
  sendMsgText($sender_id, "Спасибо, что подписались на нас!");
}
else if($input['event'] == "conversation_started")
{
  sendMsgText($sender_id, "Беседа началась!");
}
elseif($input['event'] == "message")
{
  sendMsg($sender_id, $text, $type);
}

?>