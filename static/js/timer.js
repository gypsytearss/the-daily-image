(() => {
    var time_seconds = 300;

    var countdown = document.querySelector('#timer');

    setInterval(() => {
        time_seconds = time_seconds - 1;

        var minutes_left = parseInt(Math.max(time_seconds / 60, 0)).toString();
        var seconds_left = Math.max(time_seconds % 60, 0);

        if (seconds_left < 10) {
            seconds_left = "0" + seconds_left.toString();
        }

        countdown.textContent = `${minutes_left}:${seconds_left}`;
    }, 1000);
})()