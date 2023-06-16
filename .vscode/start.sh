gunicorn main:app -w 1 --log-file -

#and app is from THIS app = Flask(__name__)