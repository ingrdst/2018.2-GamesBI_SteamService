import requests

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Game
from .serializers import GameSerializer


class SteamView(APIView):
    '''
        View that calls SteamSpy API
        and return some relevant
        information about a game
        and filter for Null value
    '''
    def get(self, request, format=None):

        Game.objects.all().delete()
        games_id = [10, 20, 5]
        for game_id in games_id:
            game_data = self.get_game_data(game_id)
            filter_game_data = self.filter_game_data(game_data)
            if filter_game_data:
                self.save_game(filter_game_data)

        games = Game.objects.all()
        games_data = []
        for game in games:
            print('------------')
            print(game.id)
            print(game.name)
            print(game.positive_reviews_steam)
            print(game.negative_reviews_steam)
            print(game.average_forever)
            print(game.average_2weeks)
            print(game.price)
            print(game.lenguages)
            print('------------')
            game_data = {
                'id': game.id,
                'name': game.name,
            }
            games_data.append(game_data)

        return Response(data=games_data)


    def get_game_data(self, game_id):
        # url = 'https://store.steampowered.com/api/appdetails?appids={}'.format(game_id)
        url = 'http://steamspy.com/api.php?request=appdetails&appid={}'.format(game_id)
        header = {'Accept': 'application/json'}
        gamedata = requests.get(url, headers=header)
        ndata = gamedata.json()
        return ndata

    def filter_game_data(self, gamedata):

        if 'appid' in gamedata:
            id = gamedata['appid']
        else:
            id = None

        if 'name' in gamedata:
            name = gamedata['name']
        else:
            name = None

        if 'positive' in gamedata:
            positive = gamedata['positive']
        else:
            positive = None

        if 'negative' in gamedata:
            negative = gamedata['negative']
        else:
            negative = None

        if 'owners' in gamedata:
            owners = gamedata['owners']
        else:
            owners = None

        if 'average_forever' in gamedata:
            average_forever = gamedata['average_forever']
        else:
            average_forever = None

        if 'average_2weeks' in gamedata:
            average_2weeks = gamedata['average_2weeks']
        else:
            average_2weeks = NoneIGDB

        if 'price' in gamedata:
            price = gamedata['price']
        else:
            price = None

        if 'languages' in gamedata:
            languages = gamedata['languages']
        else:
            languages = None

        filtered_data = {
            'id': id,
            'name': name,
            'positive_reviews_steam': positive,
            'negative_reviews_steam': negative,
            # 'owners': owners,
            'average_forever': average_forever,
            'average_2weeks': average_2weeks,
            'price': price,
            'lenguages': languages
        }
        return filtered_data


    def save_game(self, filtered_data):
        new_game = Game(
            id = filtered_data['id'],
            name = filtered_data['name'],
            positive_reviews_steam = filtered_data['positive_reviews_steam'],
            negative_reviews_steam = filtered_data['negative_reviews_steam'],
            # owners = filtered_data['owners'],
            average_forever = filtered_data['average_forever'],
            average_2weeks = filtered_data['average_2weeks'],
            price = filtered_data['price'],
            lenguages = filtered_data['lenguages'],
        )
        new_game.save()
        print('o jogo salvou ' + new_game.name)