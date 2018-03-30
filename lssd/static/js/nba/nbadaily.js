/**
 * Created by mark.huang on 2018/1/23.
 */
var is_play = false;
function play_music() {

    var audio = document.getElementById("bgMusic");
    if (is_play) {
//播放(继续播放)
        audio.pause();
        //audio.currentTime = 0;
        console.log('music','stop');
        is_play = false
    }
    else {
        audio.play();
        console.log('music','start');
        is_play = true
    }
}
