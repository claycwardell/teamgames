// Enable pusher logging - don't include this in production
Pusher.log = function(message) {
    if (window.console && window.console.log) window.console.log(message);
};


var pusher = new Pusher('ae35d633bac49aecadaf');
var channel = pusher.subscribe('herp');
channel.bind('derp', function(data) {
    $('#eat-my-shorts').append(data.name+': '+ data.message+ '<br />');

});
$('#submit_button').on('click', function(e){
    var that = this;
    var $textbox = $('#text-input');
    //submit shit to host
    $.ajax({
        "type":"POST",
        "url":"./send_message",
        data: {
            user:that.user,
            message:$textbox.val()
        }
    });
});

$('body').addClass(team);