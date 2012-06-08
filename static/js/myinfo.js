/*
 * myinfo.js
 *
 * Update and show the MySQL process information.
 *
 * The following components are required:
 *   http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js
 *   /static/js/jquery.mousewheel.js
 *   /static/js/jquery.timer.js
 */

function to_show(field) {
    // Simple function to show '---' if some field is not provided
    return field ? field : '---';
}

function update_process_list() {
    /*
     * Updates the processlist getting a JSON from the server via AJAX.
     */
    $.getJSON('/mypci', function(data) {
        var process_list = $('#process_list tbody');
        process_list.empty();
        $.each(data.process_list_info, function(i, q) {
            // Show processlist processes are not shown
            if(q.Info != 'show full processlist') {
                var row = $('<tr>');
                row.append($('<td>').append(to_show(q.Id)),
                    $('<td>').append(to_show(q.User)),
                    $('<td>').append(to_show(q.Host)),
                    $('<td>').append(to_show(q.db)),
                    $('<td>').append(to_show(q.State)),
                    $('<td>').append(to_show(q.Command)),
                    $('<td>').append(to_show(q.Time)),
                    $('<td>').append('<code>' + to_show(q.Info) + '</code>'));
                process_list.append(row);
            }
        });
    });
}

// Set a timer in order to update the process list
var timer = $.timer(update_process_list);

function timer_interval() {
    /*
     * Checks the time interval value and set it to the timer if it is correct
     */
    try {
        var control = $(this);
        var interval = parseInt(control.attr('value'));
        if(interval < 0) {
            throw "Negative time interval";
        }
        if(interval == 0) {
            timer.stop();
        } else {
            timer.set({time:interval*1000});
            timer.play();
        }
    } catch(err) {
        control.attr('value', '0');
        timer.stop();
    }
}

//Stop button event: set the counter to 0 and stop timer
$('#stop_button').click(function() {
    var control = $('#interval');
    control.attr('value', '0');
    timer.stop();
});

// Show kill input and hide kill_button
$('#kill_button').click(function() {
    $('#kill_input').show(10);
    $('#kill_button').hide(10);
});

// Try to kill a mysql process
$('#kill_now').click(function() {
    var pid = $('#kill_pid').attr('value'); 
    try {
        if(pid == '' || isNaN(pid)) {
            throw 'Empty pid';
        }
        $.post('/killprocess', {pid: pid});
        $('#kill_input').hide('fast');
        var info = $('<div>').attr({id:'info', class:'alert alert-info'});
        info.append('<a class="close" data-dismiss="alert" href="#">×</a>');
        info.append('<h4 class="alert-heading">Heads up!</h4>');
        info.append('The Kill signal has been sended to the process ' + pid + '.');
        $('h1').after(info);
        $('#kill_button').show('fast');

    } catch(err) {
        var info = $('<div>').attr({id:'info', class:'alert alert-error'});
        info.append('<a class="close" data-dismiss="alert" href="#">×</a>');
        info.append('<h4 class="alert-heading">Ooops!</h4>');
        info.append('That was an invalid Pid!');
        $('h1').after(info);
    }
});

// Events for the time's interval controller
$('#interval').change(timer_interval);
$('#interval').click(timer_interval);
$('#interval').keypress(timer_interval);
$('#interval').mousewheel(timer_interval);

