from flask import Flask
from flask_cors import CORS
from raven.contrib.flask import Sentry

from auth import auth_blueprint
from api import register
from api.user import Users
from api.scenario import Scenarios
from api.lab import Labs
from api.cloudconfig import Cloudconfigs
from api.slice import Slices
from api.configuration import Configurations
from api.flavor import Flavors

app = Flask(__name__)
app.register_blueprint(auth_blueprint, url_prefix='/auth')

app.secret_key = "joifosdjfoisjiowjroijfsldjflsjfsdopoew"

register(app, [Users, Scenarios, Labs, Cloudconfigs, Slices, Configurations, Flavors], '/api')

CORS(app)

sentry = Sentry(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
