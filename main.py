from flask import Flask, request, abort, render_template, redirect, make_response
from functools import wraps

from utils import *
from models import *


app = Flask(__name__)

def get_user(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		session = None
		user = None
		try:
			session = Session.get(session_id=request.cookies.get('session_id'))
			user = session.user
		except Session.DoesNotExist:
			pass
		return f(user=user, session=session)
	return decorated_function


@app.route("/", methods=['GET'])
@get_user
def index(*args, **kwargs):
	user = kwargs.get('user')
	return render_template('index.html', **locals())

@app.route("/begin_transaction", methods=['POST'])
def begin_transaction():
    txid = request.form.get('txid')
    postback = request.form.get('postback')
    amount = num(request.form.get('amount'))
    if txid and postback and amount:
        return "UNIMPLEMENTED"
    abort(401)

@app.route("/validate_transaction", methods=['GET'])
def validate_transaction():
    try:
        txid = Transaction.get(txid=request.form.get('txid'))
    except Transaction.DoesNotExist:
        return 'FALSE'
    return 'TRUE' if txid.paid else 'FALSE'

@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		try:
			user = User.select().where(User.email == request.form.get('email'))[0]
			password = request.form.get('password')
			if user and user.password == get_salted_password(password):
				session_id = request.cookies.get('session_id', generate_session_id())
				session = Session(user=user, session_id=session_id)
				session.save()
				response = make_response(redirect('/account'))
				response.set_cookie('session_id', session_id)
				return response
		except User.DoesNotExist:
			pass
		except IndexError:
			pass
		error = "The email and password you entered do not match."
	if request.args.get('registered'):
		message = "Registration complete! You may now login."
	return render_template('login.html', **locals())

@app.route("/logout", methods=['GET'])
@get_user
def logout(*args, **kwargs):
	user = kwargs.get('user')
	session = kwargs.get('session')
	session.active = False
	response = make_response(redirect('/?logout=true'))
	response.set_cookie('session_id', '', expires=0)
	return response

@app.route("/register", methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		first_name = request.form.get('first_name')
		last_name = request.form.get('last_name')
		email = request.form.get('email')
		password = get_salted_password(request.form.get('password'))
		User.create(first_name=first_name, last_name=last_name, email=email, password=password)
		return redirect('/login?registered=true')
	return render_template('register.html', **locals())

@app.route("/account")
@get_user
def account(*args, **kwargs):
	user = kwargs.get('user')
	return render_template('account.html', **locals())

# This hook ensures that a connection is opened to handle any queries
# generated by the request.
@app.before_request
def _db_connect():
    db.connect()

# This hook ensures that the connection is closed when we've finished
# processing the request.
@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


if __name__ == "__main__":
    app.debug = True
    db_init()
    app.run(host='0.0.0.0')
