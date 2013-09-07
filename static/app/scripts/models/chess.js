/*global define*/

define([
    'underscore',
    'backbone'
], function (_, Backbone) {
    'use strict';

    var ChessModel = Backbone.Model.extend({
        defaults: {
        }
    });

    return ChessModel;
});