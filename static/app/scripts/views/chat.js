/*global define*/

define([
    'jquery',
    'underscore',
    'backbone',
    'models/chat',
    'templates'
], function ($, _, Backbone, ChatModel, JST) {
    'use strict';

    var ChatView = Backbone.View.extend({
    	model: new ChatModel,
        template: JST['app/scripts/templates/chat.hbs'],
        initialize: function(){
        	var a = 1;
        }
    });

    return ChatView;
});