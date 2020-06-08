from flask import Flask, jsonify, request
import core.mongodb_core as cm
import core.neo4j_core as cn
from routes.cases import case_routes
from routes.deaths import death_routes
import psycopg2
app = Flask(__name__)
app.debug = True

app.register_blueprint(case_routes)
app.register_blueprint(death_routes)

# def token_required(f):
#    @wraps(f)
#    def decorator(*args, **kwargs):
#       token = None

#       if 'x-access-tokens' in request.headers:
#          token = request.headers['x-access-tokens']

#       if not token:
#          return jsonify({'message': 'a valid token is missing'})

#       try:
#          data = jwt.decode(token, app.config[SECRET_KEY])
#          current_user = Users.query.filter_by(public_id=data['public_id']).first()
#       except:
#          return jsonify({'message': 'token is invalid'})

#         return f(current_user, *args, **kwargs)
#    return decorator

# @app.route('/login', methods='POST')
# def authenticate():
#   auth = request.authorization

#   if not auth or not auth.username or not auth.password:
#      return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

#   conn = psycopg2.connect('host=postgres dbname=covid user=postgres password=12345678')
#   cur = conn.cursor()
#   cur.execute('SELECT * FROM users WHERE name=%s', [username])
#   user = cur.fetchone()
#   conn.close()

#   if check_password_hash(user.password, auth.password):
#      token = jwt.encode({'sub': user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'oausdnoaisdioasdu')
#      return jsonify({'token' : token.decode('UTF-8')})

#   return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


# @app.route('/setup')
# def setup():
#     try:
#         conn = psycopg2.connect('host=postgres dbname=covid user=postgres password=12345678')
#         cur = conn.cursor()
#         cur.execute('DROP TABLE IF EXISTS users; CREATE TABLE users (id int PRIMARY KEY, name varchar, password varchar);')
#         cur.execute("INSERT INTO users (id, name) VALUES (1, 'admin', '), (2, 'manager');")
#         conn.commit()
#         cur.close()
#         conn.close()

#         return 'Setup successful'
#     except:
#         return 'An exception occurred'


@app.route('/refresh')
def sync_data():
    return cn.sync_data()


@app.route('/')
def hello_world():
    return cm.add_initial_covid_data()
