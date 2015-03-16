var url = "https://www.youtube.com/embed/DEMO_ID?autoplay=1&amp;controls=0&amp;loop=1&amp;disablekb=1&amp;modestbranding=1&amp;showinfo=0&amp;enablejsapi=1";
var demo_ids = ['xTBQfwVUXvM', 'ZlphVz2Udns', 'PPMPgPMwCEw', 'PzNckOi8m2Y', 'lXtC9_iSKCM'];
var player = document.getElementById('player');
var random_demo = demo_ids[Math.floor(Math.random() * demo_ids.length)];
player.src = url.replace('DEMO_ID', random_demo);

// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');
tag.src = "http://www.youtube.com/player_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player;
function onYouTubePlayerAPIReady() {
  player = new YT.Player('player', {
    playerVars: { 'autoplay': 1, 'controls': 1,'autohide':1,'wmode':'opaque' },
    videoId: 'JW5meKfy3fY',
    events: {
      'onReady': onPlayerReady}
  });
}

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
  event.target.mute();
}
