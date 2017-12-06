from games.models import Game
from games.serializers import GameSerializer
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@csrf_exempt
@api_view(http_method_names=['GET', 'POST'])
def game_list(request):
    if request.method == 'GET':
        games = Game.objects.all()
        games_serializer = GameSerializer(games, many=True)
        return Response(games_serializer.data)
    elif request.method == 'POST':
        game_serializer = GameSerializer(data=request.data)
        if game_serializer.is_valid():
            game_serializer.save()
            return Response(game_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(game_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(http_method_names=['GET', 'POST', 'PUT'])
def game_detail(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        game_serialized_data = GameSerializer(game)
        return Response(game_serialized_data.data)
    elif request.method == 'PUT':
        game_serializer = GameSerializer(game, data=request.data)
        if game_serializer.is_valid():
            game_serializer.save()
            return Response(game_serializer.data)
        return Response(game_serializer.data,
                        status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
