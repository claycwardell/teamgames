/*global require*/
'use strict';

require.config({
    shim: {
        underscore: {
            exports: '_'
        },
        backbone: {
            deps: [
                'underscore',
                'jquery'
            ],
            exports: 'Backbone'
        },
        bootstrap: {
            deps: ['jquery'],
            exports: 'jquery'
        },
        handlebars: {
            exports: 'Handlebars'
        }
    },
    paths: {
        jquery: '../bower_components/jquery/jquery',
        backbone: '../bower_components/backbone/backbone',
        underscore: '../bower_components/underscore/underscore',
        bootstrap: 'vendor/bootstrap',
        handlebars: '../bower_components/handlebars/handlebars'
    }
});

require([
    'backbone',
    'views/app_view',
    'models/chat'
],
function(Backbone, AppView, chat_model) {
    Backbone.history.start();

    var Chat_Model = new chat_model();
    window.AppView = new AppView({el:$('#app'), chat_model: Chat_Model});
});