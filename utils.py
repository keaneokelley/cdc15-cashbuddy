import datetime, random
from requests_futures.sessions import FuturesSession

def num(s):
    try:
        return int(s)
    except (ValueError, TypeError):
        return None

def generate_session_id():
	return str(random.randint(1,2000)) + 'test'

def get_salted_password(password):
	return password + 'sajd134kj2rv423J2z3@$#mnfmdj3m2Dn3ehfjdnklm$@#REKGlhjkJFDcdsjkh'

def do_postback(txid, postback):
    # Do asynchronously with futures so the user doesn't have to wait.
    session = FuturesSession()
    url = 'http://' + postback
    data = {
            'txid': txid,
            'paid': 'TRUE',
            }
    r = session.post(url, data=data)
