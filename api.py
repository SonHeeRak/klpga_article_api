from flask import Flask,  render_template
from flask_restful import Api
from flask_cors import CORS

import config as c

from core.log_helper import LogHelper
from core.response_helper import ResponseHelper
# from core.background_thread_helper import BackgroundThreadHelper

from report.player_article.controllers import PlayerControllers as PlayerArticle

from core.cache_helper import CacheHelper
from report.common_lib import globals as g

app = Flask(__name__)
CORS(app)
api = Api(app)

CacheHelper().init(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

# KLPGA 선수별 기사
@app.route("/player_article/<tour_id>/<p_id>/<round_no>")
def player_test(p_id, tour_id, round_no):
    g.initialize()  # <TODO> 개발때만 쓰고 지워라!
    result = PlayerArticle(p_id=int(p_id), tour_id=tour_id, round_no=int(round_no)).generate_article()
    return ResponseHelper().write(result)


if __name__ == '__main__':
    try:
        LogHelper.instance().i('Server Start')
        g.initialize()

        app.run(debug=True, host='127.0.0.1', port=21215)

    except Exception as ex:
        LogHelper.instance().e(ex)
