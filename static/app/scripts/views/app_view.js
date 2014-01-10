/*global define*/

define([
    'jquery',
    'underscore',
    'backbone',
    'views/chess',
    'views/chat',
    'templates'
], function ($, _, Backbone, ChessView, ChatView, JST) {
    'use strict';

    var AppViewView = Backbone.View.extend({
        template: JST['app/scripts/templates/app_view.hbs'],
        events: {
        	'click #submit-message': 	'on_submit_message_click',
        	'keydown #text-input': 		'message_key_down',
        	'click #submit-username': 	'on_submit_username_click'
        },
        initialize: function(options){
        	_.bindAll(this, 'render', 'append_message', 'on_submit_message_click',  
        		'start_request_username');
        	this.model = options.chat_model;

        	this.render();


        	this.model.bind('change:team', this.add_team);


        	// CHAT SETUP

        	// get username
        	this.model.fetch();

        	this.model.bind('new_message', this.append_message);


        	// init setup for username once model has synced
        	this.model.once('change:username', function(){
        		if(this.model.get('username')=="None"){
			        this.start_request_username();
			    }
        	}, 
        	this);

        	//DEBUG
        	//this.model.start_messages_text();
        	

            // CHESS SETUP
            this.setup_game();


		    
        },
        setup_game: function(){
            if(typeof(this.game_view)=="undefined"){
                this.game_view = new ChessView({
                    el: this.$('#chess_container')
                });
                this.$('#chess_container').append(this.game_view.el);
                this.game_view.bind('player_changed', this.player_changed)
            }
            this.game_view.render();
        },
        player_changed: function(user_is_player_bool){
            if( user_is_player_bool ){
                alert('you are the player')
            }
            else{
                alert('you are no longer the player');
            }
        },
        add_team: function(){
            $('body').addClass(this.model.get('team'));
        },
        render: function(){
        	this.$el.html(this.template(this.model.toJSON()));
        	
        }, 
        // chess functions



        // chat functions
        append_message: function(data_as_string){
        	var scrolled_to_btm = this.$('#chat-box').scrollTop()==this.$('#chat-box').height()
        	this.$('#chat-box').append(data_as_string);
        	this.scroll_behavior(scrolled_to_btm);
        },
        scroll_behavior: function(scrolled_to_btm){
        	// if scroll bar is at btm, keep it at btm
        	if(scrolled_to_btm){
        		var a = 1+2;
        	}
        },
        on_chat_box_scroll_debouced: function(e){
        	// if we are at the end, keep scroll bar at btm

        	// if we are not at the end, keep scroll bar in current position
        },
        message_key_down: function(e){
        	if(e.keyCode == 13){
		        this.on_submit_message_click();
		    }
        },
        on_submit_message_click: function(e){
        	// check if we have a username
		    if( !this.model.get('username') ){
		        this.start_request_username();
		    }
		    // submit via post request
		    else{
		        this.submit_message();
		    }
        },
        submit_message: function(){
		    var that = this
		    var message = this.$('#text-input').val();
		    var username = this.model.get('username');

		    this.model.submit_message(
		    	message, 
		    	username, 
		    	function(){that.$('#text-input').val('');}
		    );
		    
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
		    this.$el.append(current_popup);
		},
		on_submit_username_click: function(){
		    var selected_username = $('#username-input').val();
		    this.model.submit_username(selected_username, error_function);
		    

		    function error_function(){
		        $('#username-input-caption').text('That username was taken, try another');
		        $('#username-input').val('');
		    }
		}
		
    });

    return AppViewView;
});