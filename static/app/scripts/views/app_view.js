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
        initialize: function(options){
        	_.bindAll(this, 'render', 'append_message', 'on_submit_message_click',  
        		'start_request_username');
        	this.model = options.chat_model;

        	this.render();


        	this.model.bind('change', this.render);
        	// get username
        	this.model.fetch();

        	this.model.bind('new_message', this.append_message);


        	// init setup for username once model has synced
        	this.model.once('change', function(){
        		if(this.model.get('username')=="None"){
			        this.start_request_username();
			    }
        	}, 
        	this);
        	

		    
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