/*global define*/

define([
    'jquery',
    'underscore',
    'backbone',
    'templates'
], function ($, _, Backbone, JST) {
    'use strict';

    var ChatView = Backbone.View.extend({
        template: JST['app/scripts/templates/chat.hbs']
    });

    return ChatView;
});