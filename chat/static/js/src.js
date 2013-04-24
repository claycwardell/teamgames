function init(){
    $('body').addClass(team);
    // Enable pusher logging - don't include this in production
    Pusher.log = function(message) {
        if (window.console && window.console.log) window.console.log(message);
    };


    var pusher = new Pusher('ae35d633bac49aecadaf');
    var channel = pusher.subscribe('herp');
    channel.bind(team, function(data) {
        $('#chat-box').append(data.name+': '+ data.message+ '<br />');

    });

    start_request_username()

};

init();



function get_username(){
    return username;
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
    var message = $('#text-input').val();
    var username = get_username();
    $.ajax({
        "type":"POST",
        "url":"./new_message/",
        data: JSON.stringify({
            username:username,
            message:message
        })
    });
}

function on_submit_username_click(){

    var selected_username = $('#username-input').val();
    $.ajax({
        "type":"POST",
        "url":"./set_username/",
        data: JSON.stringify({
            username:selected_username
        }),
        success: function(response){
            // set username
            if(response.success){
                username = selected_username;
                $('#player_name').text(selected_username);
                window.current_popup.remove();
                window.current_popup = undefined;
            }
            else{
                errorfunction();
            }

        },
        error: function(one, two, three){
            // username taken, try again
            errorfunction();
        }
    })
    function errorfunction(){
        $('#username-input-caption').text('That username was taken, try another');
        $('#username-input').val('');
    }
}

function start_request_username(){
    // create popup
    var popup = $('' +
        '<div id="popup-wrapper">' +
            '<div id="popup">' +
                '<p id="username-input-caption">Please enter a username</p>' +
                '<input id="username-input" type="text">' +
                '<button id="submit_username">Submit</button> ' +
            '</div> ' +
        '</div>');

    popup.remove_popup = function(){
        //remove popup from dom
        //take care of event listeners?
    }

    window.current_popup = popup;
    $('body').append(current_popup);

    //
}

// event bindings
$('#submit_message').on('click', on_submit_message_click);
$('#submit_username').on('click', on_submit_username_click);


