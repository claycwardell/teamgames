/*global define*/

define([
    'jquery',
    'underscore',
    'backbone',
    'templates'
], function ($, _, Backbone, JST) {
    'use strict';

    var AppViewView = Backbone.View.extend({
        template: JST['app/scripts/templates/app_view.hbs'],
        events: {
        	'click #submit_message': 	'on_submit_message_click',
        	'keydown #text_input': 		'message_key_down',
        	'click #submit_username': 	'on_submit_username_click'
        },
        username:'None',
        active: True,
        initialize: function(options){
        	_.bindAll(this, 'render', 'append_message', 'on_submit_message_click', 
        		'on_submit_username_click', 'submit_message',
        		'get_username', 'start_request_username', 'start_active_check_timer', 'ping_is_active');
        	this.model = options.chat_model;

        	this.render();


        	this.model.bind('change', this.render);
        	this.model.fetch();

        	this.model.bind('new_message', this.append_message);

        	if(this.username=="None"){
		        this.start_request_username()
		    }
		    else{
		        this.set_username(username)
		    }

		    this.start_active_check_timer();
        },
        render: function(){
        	this.$el.html(this.template(this.model.toJSON()));
        	$('body').addClass(this.model.get('team'));
        }, 
        append_message: function(data_as_string){
        	this.$('#chat-box').append(data_as_string);
        },
        message_key_down: function(e){
        	if(e.keyCode == 13){
		        this.on_submit_message_click();
		    }
        },
        on_submit_message_click: function(e){
        	// check if we have a username
		    if( !get_username() ){
		        start_request_username();
		    }
		    // submit via post request
		    else{
		        submit_message();
		    }
        },
        submit_message: function(){
		    var that = this
		    var message = this.$('#text-input').val();
		    var username = get_username();
		    $.ajax({
		        "type":"POST",
		        "url":"./api/new_message/",
		        data: JSON.stringify({
		            username:username,
		            message:message
		        }),
		        success: function(){
		            this.$('#text-input').val('');
		        }
		    });
		},
		get_username: function(){
		    return this.username;
		},
		start_request_username: function(){
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
		},
		on_submit_username_click: function(){
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
		                set_username(selected_username)
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
		},
		start_active_check_timer: function(){
			var that = this;
		    setInterval (do_check, 60000);
		    function do_check(){
		        if(that.active){
		            ping_is_active();
		        }
		    }
		}
		ping_is_active: function(){
			var that = this;
		    $.ajax({
		        type: 'GET',
		        url: './ping',
		        success: function(resp){
		            if(resp.success){
		                if(resp.player){
		                    alert('you are now the player');
		                    that.player = true;
		                }
		            }
		        }
		    })
		}
    });

    return AppViewView;
});