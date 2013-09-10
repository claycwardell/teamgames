/*global define*/

define([
    'underscore',
    'backbone'
], function (_, Backbone) {
    'use strict';

    var ChatModel = Backbone.Model.extend({
        defaults: {
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
		}

    });

    return ChatModel;
});