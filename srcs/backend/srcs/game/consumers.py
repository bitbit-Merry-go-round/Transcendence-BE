from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Game, GameInfo


class GameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        try:
            self.game_id = self.scope["url_route"]["kwargs"]["game_id"]

            if not await self.check_game_exists(self.game_id):
                raise ValueError("game does not exist.")

            game_name = self.get_game_name(self.game_id)

            await self.channel_layer.group_add(game_name, self.channel_name)
            await self.accept()

        except ValueError as e:
            await self.send_json({"error": str(e)})
            await self.close()

    async def disconnect(self, close_code):
        try:
            game_name = self.get_game_name(self.game_id)
            await self.channel_layer.group_discard(game_name, self.channel_name)

        except Exception as e:
            pass

    async def receive_json(self, content):
        try:
            paddle_pos_x = content["paddle_pos_x"]
            paddle_pos_y = content["paddle_pos_y"]
            ball_pos_x = content["ball_pos_x"]
            ball_pos_y = content["ball_pos_y"]
            player_one = content.get("player_one")
            player_two = content.get("player_two")

            if not player_one or not player_two:
                raise ValueError("both players must exist.")

            game = await self.get_or_create_game(player_one, player_two)

            self.game_id = str(game.id)

            game_name = self.get_game_name(self.game_id)

            # await self.save_game_info(game, paddle_pos_x, paddle_pos_y, ball_pos_x, ball_pos_y)

            await self.channel_layer.group_send(game_name, {
                "type": "game_info",
                "paddle_pos_x": paddle_pos_x,
                "paddle_pos_y": paddle_pos_y,
                "ball_pos_x": ball_pos_x,
                "ball_pos_y": ball_pos_y,
            })

        except ValueError as e:
            await self.send_json({"error": str(e)})

    async def game_info(self, event):
        try:
            paddle_pos_x = event["paddle_pos_x"]
            paddle_pos_y = event["paddle_pos_y"]
            ball_pos_x = event["ball_pos_x"]
            ball_pos_y = event["ball_pos_y"]

            await self.send_json({
                "paddle_pos_x": paddle_pos_x,
                "paddle_pos_y": paddle_pos_y,
                "ball_pos_x": ball_pos_x,
                "ball_pos_y": ball_pos_y,
            })
        except Exception as e:
            await self.send_json({"error": str(e)})

    @staticmethod
    def get_game_name(game_id):
        return f"game_{game_id}"

    @database_sync_to_async
    def get_or_create_game(self, player_one, player_two):
        game, created = Game.objects.get_or_create(
            player_one=player_one,
            player_two=player_two
        )
        return game

    @database_sync_to_async
    def save_game_info(self, game, paddle_pos_x, paddle_pos_y, ball_pos_x, ball_pos_y):
        GameInfo.objects.create(game=game,
                                paddle_pos_x=paddle_pos_x,
                                paddle_pos_y=paddle_pos_y,
                                ball_pos_x=ball_pos_x,
                                ball_pos_y=ball_pos_y)

    @database_sync_to_async
    def check_game_exists(self, game_id):
        return Game.objects.filter(id=game_id).exists()
