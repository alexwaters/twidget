from flask_restful import Resource, reqparse
from flask import jsonify
import config
import requests
import json
import requests_cache
import time

now = time.ctime(int(time.time()))
base_url = 'https://api.twitch.tv/kraken/'
client_id = config.client_id

requests_cache.install_cache('twitch_cache', backend='sqlite', expire_after=180)

class TwitchGames(Resource):
    # for streaming see http://stackoverflow.com/questions/18082683/need-to-execute-a-function-after-returning-the-response-in-flask
    def multiple_reqs(self, games):
        limit = 100
        total = TwitchTotalGames.get()
        if games == "max":
            games = total
        calls = (games // limit)
        rem = games % limit
        if rem > 0:
            calls += 1
        game_list = []
        for i in range(calls):
            offset = limit * i
            r = requests.get(
                base_url + 'games/top?limit=100' + '&offset=' + str(offset),
                headers={'Client-ID': client_id})
            print "Time: {0} / Used Cache: {1}".format(now, r.from_cache)
            game_list += (json.loads(r.text)["top"])
            print i
        return game_list

    def get(self, limit=400, offset=0):
        if limit > 100 or limit == "max":
            games = self.multiple_reqs(limit)
        else:
            r = requests.get(
                base_url + 'games/top?limit=' + str(limit) + '&offset=' + str(offset),
                headers={'Client-ID': client_id})
            print "Time: {0} / Used Cache: {1}".format(now, r.from_cache)
            games = json.loads(r.text)["top"]
        return jsonify(games)


class TwitchTotalGames(Resource):
    @staticmethod
    def get():
        r = requests.get(
            base_url + 'games/top?limit=1',
            headers={'Client-ID': client_id})
        print "Time: {0} / Used Cache: {1}".format(now, r.from_cache)
        return json.loads(r.text)['_total']
