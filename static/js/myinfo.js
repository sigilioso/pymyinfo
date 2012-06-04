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
            if(q.Info != 'show processlist') {
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

// Events for the time's interval controller
$('#interval').change(timer_interval);
$('#interval').click(timer_interval);
$('#interval').keypress(timer_interval);
$('#interval').mousewheel(timer_interval);

