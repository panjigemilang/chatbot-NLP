<?php
require_once __DIR__ . '/lineBot.php';

// Bot
$bot = new Linebot();
$text = $bot->getMessageText();
$bot->reply($text);

// getUserId
$userId = $bot->getUserId();

// pushText
$bot->pushText($userId, "Hello username");

// pushImage
$imageUrl = "https://ibb.co/VHmHNhP";
$bot->pushImage($userId, $imageUrl);

// pushVideo
$videoUrl = "https://www.youtube.com/watch?v=PGbAWTqUuxQ";
$coverImage = "https://example.com/cover.jpg";
$bot->pushVideo($userId, $videoUrl, $coverImage);