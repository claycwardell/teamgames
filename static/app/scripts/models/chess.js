/*global define*/

define([
    'underscore',
    'backbone'
], function (_, Backbone) {
    'use strict';

    var ChessModel = Backbone.Model.extend({
        defaults: {
        },
        url: function(){
        	return 'api/chess'
        },
        initialize: function(){
        	var default_game_board = this.get_default_game_board();
        	this.set('game_board', default_game_board);
        },
		start_pusher_chat: function(){
			if(this.get('team')!='teamless'){
				alert('pusher for chess game not set');
				var pusher = new Pusher('');
			    var channel = pusher.subscribe(this.get('team'));
			    channel.bind('new-message', this.on_new_message);
			}
			
		},
		on_new_message: function(data){
			var user = window.get_current_user();
		    if(!user.player && data.player == user.username){
		        this.trigger('player_changed', true)
		    }
		    this.update_board_with_move(data.move);
		},
		update_board_with_move: function(move){
			this.trigger('chess_move', move);
		},
		get_default_game_board: function(){
			var game_board = [];
			for (var row = 0; row < 8; row ++){
				game_board[row] = []
				for (var column = 0; column < 8; column ++){
					// PIECE TYPE
					var piece = {};
					if(row>1 && row<6){
						game_board[row].push(piece);
						continue;
					}
					if(column==3){
						if(row==0){
							piece.type='K';
						}
						else{
							piece.type='Q';
						}
					}
					else if(column==4){
						if(row==0){
							piece.type='Q';
						}
						else{
							piece.type='K';
						}
					}
					if(column==0 || column==7){
						piece.type = 'R';
					}
					else if(column==1 || column==6){
						piece.type = 'B';
					}
					else if(column==2 || column==5){
						piece.type = 'N';
					}
					if (row==1 || row==6){
						piece.type = 'P';
					}


					// OWNER
					if(row < 3){
						piece.owner = 'white';
					}
					else{
						piece.owner = 'black';
					}

					// APPEND PIECE
					game_board[row].push(piece);
				}
			}

			return game_board;
			
		}

    });

    return ChessModel;
});

