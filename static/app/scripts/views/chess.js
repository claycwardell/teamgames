/*global define*/

define([
    'jquery',
    'underscore',
    'backbone',
    'models/chess',
    'templates'
], function ($, _, Backbone, ChessModel, JST) {
    'use strict';

    var ChessView = Backbone.View.extend({
    	model: new ChessModel,
        template: JST['app/scripts/templates/chess.hbs'],
        initialize: function(){
        	var a = 1;
        	this.model.bind('chess_move', this.render);
        },
        render: function(){
        	this.$el.html(this.template(this.model.toJSON()));

        	// Draw game board
        	this.render_game_board();
        	

			// Draw pieces
			this.render_game_pieces();

        },
        render_game_board: function(){
        	var canvas = document.getElementById("game_board");
			var context2D = canvas.getContext("2d");
			var square_size = this.$el.height()/8

			for (var row = 0; row < 8; row ++){
				for (var column = 0; column < 8; column ++)
				{
					// coordinates of the top-left corner
					var x = column * square_size;
					var y = row * square_size;

					if (row%2 == 0){
						if (column%2 == 0)
						{
							context2D.fillStyle = "white";
						}
						else
						{
							context2D.fillStyle = "black";
						}
					}
					else{
						if (column%2 == 0){
							context2D.fillStyle = "black";
						}
						else
						{
							context2D.fillStyle = "white";
						}
					}

					context2D.fillRect(x, y, square_size, square_size);
				}
			}
        },
        render_game_pieces: function(){
        	var game_board = this.model.get('game_board');
        	for (var row = 0; row < 8; row ++){
        		var row_string = ''
				for (var column = 0; column < 8; column ++){
					var piece_type;
					if(typeof(game_board[row][column].type)=="undefined"){
						piece_type=' ';
					}
					else{
						piece_type=game_board[row][column].type;
					}
					row_string+='['+piece_type+']';

					if(piece_type!=' '){
						/*
						if(game_piece.owner=='white'){

						}
						else{

						}
						drawing = new Image();
						drawing.src = "draw.png";
						drawing.onload = function() {
						   context.drawImage(drawing,0,0);
						}
						*/
					}
				}
				console.log(row_string);
			}

        }
    });

    return ChessView;
});