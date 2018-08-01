from flask import Flask, render_template
from flask_restful import Api
import app_api, config

app = Flask(__name__)
app.secret_key = config.secret_key
api = Api(app)


@app.route("/")
def index():
    return render_template("index.html", client_id=config.client_id, ga_id=config.google_analytics_id)

# could do an iterator here like for each function in app_api do add_resource
api.add_resource(app_api.TwitchGames, '/twitch_games')
api.add_resource(app_api.TwitchTotalGames, '/twitch_total_games')


if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        print e
