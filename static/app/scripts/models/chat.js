/*global define*/

define([
    'underscore',
    'backbone'
], function (_, Backbone) {
    'use strict';

    var ChatModel = Backbone.Model.extend({
        defaults: {
        	username: 'None',
        	team: null,
        	active: true
        },
        url: function(){
			return './api/chat/'
		},
		initialize: function(){
			_.bindAll(this, 'log_change', 'save_team', 
				'start_pusher_chat', 'on_new_message',
				'start_messages_text', 'parse_chat_commands');

			this.on('change', this.log_change);
			this.on('change:team', this.save_team);

			// DEBUGGING, remove later
			//this.set('team', 'red');
			this.start_active_check_timer();
		},
		start_messages_text: function(){
			var that = this;
			var test_messages = [
				{sender:'Clay', message:'A test of the @ functionality: @Tom you are so cool.'},
				{sender:'Tom', 	message:'A short test message'},
				{sender:'Tom', 	message:'A slightly longer test message @Tom9, @Tom0'},
				{sender:'Tom', 	message:'This test message should be multiple lines long. This test message should be multiple lines long. This test message should be multiple lines long. This test message should be multiple lines long. '},
				{sender:'Tom', 	message:'A short test message'},
				{sender:'Clay', message:'A test message from another user'},
				{sender:'Clay', message:'A test of the @ functionality: @Tom you are so cool.'},
				{sender:'Tom', 	message:'This test message should be multiple lines long. This test message should be multiple lines long. This test message should be multiple lines long. This test message should be multiple lines long. '},
				{sender:'Tom', 	message:'This test message should be multiple lines long. This test message should be multiple lines long. This test message should be multiple lines long. This test message should be multiple lines long. '},
				{sender:'Tom', 	message:'This test message should be multiple lines long. This test message should be multiple lines long. This test message should be multiple lines long. This test message should be multiple lines long. '},
				{sender:'Tom', 	message:'This test message should be multiple lines long. This test message should be multiple lines long. This test message should be multiple lines long. This test message should be multiple lines long. '},
				{sender:'Tom', 	message:'This test message should be multiple lines long. This test message should be multiple lines long. This test message should be multiple lines long. This test message should be multiple lines long. '},
				{sender:'Tom', 	message:'Hopefully that is enough to test scrolling in the chat box. '},
				

			];
			function myTimeoutFunction()
			{
			    that.on_new_message(test_messages.shift());
			    if(test_messages.length){
			    	setTimeout(myTimeoutFunction, 1000);
			    }
			}
			myTimeoutFunction();
		},
		log_change: function(){
			console.log(this.toJSON());
		},
		save_team: function(){
			this.start_pusher_chat();
		},
		start_pusher_chat: function(){
			if(this.get('team')!='teamless'){
				var pusher = new Pusher('ae35d633bac49aecadaf');
			    var channel = pusher.subscribe(this.get('team'));
			    channel.bind('new-message', this.on_new_message);
			}
			
		},
		on_new_message: function(data){
			var sender;
		    if(data.player){
		        sender = '[P]'+data.sender;
		    }
		    else{
		        sender = data.sender;
		    }
		    var message_text = (
		    	'<span class="message">'+
			    	'<span class="username">'+sender+'</span>: '+ 
			    	'<span class="msg-content">'+data.message+ '</span>'+
		    	'</span>');
		    message_text = this.parse_chat_commands(message_text);
	        this.trigger('new_message', message_text);
		},
		parse_chat_commands: function(message_text){
			// split message into parts we want to parse
			var $message_text = $(message_text);
			var $message_content = $message_text.find('.msg-content')

			// find @username
			if(this.get("username")=="None"){	
				return;
				// your username
			}
			var username_re = new RegExp("@"+this.get("username"));	
			var username_search = $message_content.text().match(username_re);
			if(username_search!=null){
				if(username_search.length){
					// message content html as string
					var mchas = $("<div />").append($message_content.clone()).html();
					for( var i in username_search){
						// find and replace result with new tag
						mchas = mchas.replace(username_search[i], '<span class="highlighted_username">'+username_search[i]+'</span>');
					}
					$message_content = $(mchas);
				}
				
			}
			
			// replace with new message_content
			$message_text.find('.msg-content').replaceWith($message_content);

			// get entire message_text and convert back to html as string
			message_text = $("<div />").append($message_text.clone()).html();
			return message_text;

		},
		submit_message: function(message, username, success_function){
			$.ajax({
		        "type":"POST",
		        "url":"./api/chat/new_message/",
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
			var that = this;
			$.ajax({
		        "type":"POST",
		        "url":"./api/chat/set_username/",
		        data: JSON.stringify({
		            username:selected_username
		        }),
		        success: function(response){
		            if(response.success){
		                that.set('username', selected_username)
		            }
		            else{
		                error_fplayerunction();
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
		    setInterval (do_check, 9000);
		    function do_check(){
		        if(that.get('active')){
		            that.ping_is_active();
		        }
		    }
		},
		ping_is_active: function(){
			var that = this;
		    $.ajax({
		        type: 'GET',
		        url: './api/chat/ping/',
		        success: function(resp){
		            if(resp.success){
		                if(resp.player){
		                	if(that.get('player')==false){
		                		alert('you are now the player');
		                	}
		                    that.set('player', true);
		                }
		            }
		        }
		    })
		}

    });

    return ChatModel;
});