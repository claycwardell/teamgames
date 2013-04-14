function init(){
    $('body').addClass(team);
    // Enable pusher logging - don't include this in production
    Pusher.log = function(message) {
        if (window.console && window.console.log) window.console.log(message);
    };


    var pusher = new Pusher('ae35d633bac49aecadaf');
    var channel = pusher.subscribe('herp');
    channel.bind('derp', function(data) {
        $('#eat-my-shorts').append(data.name+': '+ data.message+ '<br />');

    });

    start_request_username()

};

init();



function get_username(){
    return window.username;
}
function on_submit_message_click(e){
    // check if we have a username
    if( !get_username() ){
        start_request_username();
    }
    // submit via post request
    else{
        submit_message();
    }
}
function submit_message(){
    var that = this
    var $textbox = $('#text-input');
    $.ajax({
        "type":"POST",
        "url":"./send_message",
        data: {
            user:that.user,
            message:$textbox.val()
        }
    });
}

function on_submit_username_click(){

    var username = $('#username-input').val();
    $.ajax({
        "type":"POST",
        "url":"./set_username/",
        data: JSON.stringify({
            username:username
        }),
        success: function(response){
            // set username
            window.username = username;
            window.current_popup.remove();
            window.current_popup = undefined;
        },
        error: function(one, two, three){
            // username taken, try again
            var a = 1;
        }
    })
}

function start_request_username(){
    // create popup
    window.current_popup = $('' +
        '<div id="popup-wrapper">' +
            '<div id="popup">' +
                '<p>Please enter a username</p>' +
                '<input id="username-input" type="text">' +
                '<button id="submit_username">Submit</button> ' +
            '</div> ' +
        '</div>');
    $('body').append(current_popup);

    //
}

// event bindings
$('#submit_message').on('click', on_submit_message_click);
$('#submit_username').on('click', on_submit_username_click);


