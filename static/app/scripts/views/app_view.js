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
        initialize: function(){
        	_.bindAll(this, 'render');
        	this.chatmodel = Backbone.Model.extend({
        		url: function(){
        			return 'http://localhost:9000/api/chat/'
        		},
        		initialize: function(){
        			this.on('change', this.log_change);
        		},
        		log_change: function(){
        			console.log(this.toJSON());
        		}
        	});
        	this.model = new this.chatmodel();

        	this.render();


        	this.model.bind('change', this.render);
        	this.model.fetch();
        },
        render: function(){
        	this.$el.html(this.template(this.model.toJSON()));
        	$('body').addClass(this.model.get('team'));
        }
    });

    return AppViewView;
});