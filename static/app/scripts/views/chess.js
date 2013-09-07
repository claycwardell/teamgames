/*global define*/

define([
    'jquery',
    'underscore',
    'backbone',
    'templates'
], function ($, _, Backbone, JST) {
    'use strict';

    var ChessView = Backbone.View.extend({
        template: JST['app/scripts/templates/chess.hbs']
    });

    return ChessView;
});