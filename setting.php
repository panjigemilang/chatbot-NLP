<?php

class Setting {
	public static function getChannelAccessToken(){
		$channelAccessToken = "1566577478";
		return $channelAccessToken;
	}
	public static function getChannelSecret(){
		$channelSecret = "59e53e706d6f697d707e96afcdb9a359";
		return $channelSecret;
	}
	public static function getApiReply(){
		$api = "https://api.line.me/v2/bot/message/reply";
		return $api;
	}
	public static function getApiPush(){
		$api = "https://api.line.me/v2/bot/message/push";
		return $api;
	}
}
