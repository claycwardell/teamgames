/*global define*/

define([
    'underscore',
    'backbone'
], function (_, Backbone) {
    'use strict';

    var ChatModel = Backbone.Model.extend({
        defaults: {
        	username: 'None',
        	active: true
        },
        url: function(){
			return 'http://localhost:9000/api/chat/'
		},
		initialize: function(){
			_.bindAll(this, 'log_change', 'save_team', 'start_pusher_chat', 'on_new_message');

			this.on('change', this.log_change);
			this.on('change:team', this.save_team);
		},
		log_change: function(){
			console.log(this.toJSON());
		},
		save_team: function(){
			window.localhost.save({'team':this.get('team')});
			this.start_pusher_chat();
		},
		start_pusher_chat: function(){
			var pusher = new Pusher('ae35d633bac49aecadaf');
		    var channel = pusher.subscribe(team);
		    channel.bind('new-message', this.on_new_message);
		},
		on_new_message: function(data){
			var sender;
		    if(data.player){
		        sender = '[P]'+data.sender;
		    }
		    else{
		        sender = data.sender;
		    }
		    var message_text = (sender+': '+ data.message+ '<br />');
	        this.trigger('new_message', message_text);
		},
		submit_message: function(message, username, success_function){
			$.ajax({
		        "type":"POST",
		        "url":"./api/new_message/",
		        data: JSON.stringify({
		            username:username,
		            message:message
		        }),
		        success: function(){
		            success_function();
		        }
		    });
		},
		submit_username: function( selected_username, error_function){
			$.ajax({
		        "type":"POST",
		        "url":"./api/set_username/",
		        data: JSON.stringify({
		            username:selected_username
		        }),
		        success: function(response){
		            if(response.success){
		                set_username(selected_username)
		            }
		            else{
		                error_function();
		            }

		        },
		        error: function(one, two, three){
		            // username taken, try again
		            error_function();
		        }
		    })
		},
		start_active_check_timer: function(){
			var that = this;
		    setInterval (do_check, 60000);
		    function do_check(){
		        if(that.get('active'){
		            ping_is_active();
		        }
		    }
		},
		ping_is_active: function(){
			var that = this;
		    $.ajax({
		        type: 'GET',
		        url: './ping',
		        success: function(resp){
		            if(resp.success){
		                if(resp.player){
		                    alert('you are now the player');
		                    that.set('player', true);
		                }
		            }
		        }
		    })
		}

    });

    return ChatModel;
});