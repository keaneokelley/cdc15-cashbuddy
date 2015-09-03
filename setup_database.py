from models import *
from utils import *

db_init()
u = User.create(username="cdc", password=get_password('cdc'), balance=10000)
c = Card.create(user=u, number="8675-3098-2857-3298", pin="123")
c1 = Card.create(user=u, number="7390-2571-9385-7193", pin="249")
t = Transaction.create(user=u, amount=9.99, dest="Loogle", paid=True, txid="43rtgfb")
t1 = Transaction.create(user=u, amount=500, dest="Safari LLC", paid=True, txid="sfadf23")
t2 = Transaction.create(user=u, amount=17.67, dest="Coldway Bakery", paid=False, txid="wereufvn")
bob = User.create(username='bob', password=get_password('cdc'), balance=10000)
bill = User.create(username='bill_musk', password=get_password('cdc'), balance=1500000)
elon = User.create(username='elon_gates', password=get_password('cdc'), balance=1250000)
fred = User.create(username='fred', password=get_password('bubbles'), balance=5000)
george = User.create(username='george', password=get_password('taco'), balance=5000)
henry = User.create(username='henry', password=get_password('ILikeTurtles'), balance=5000)
irene = User.create(username='irene', password=get_password('MittensTheKitten'), balance=2500)
Catchphrase.create(text="The freedom to pay anywhere without worry. We've got you covered.")
Catchphrase.create(text="If it's not CashBuddy, it's not secure.")
Catchphrase.create(text="If it's not secure, it's not CashBuddy.")
Catchphrase.create(text="Security is our middle name.")
Catchphrase.create(text="Making it easier to pay, everyday.")
s = Session.create(user=u, session_id="1590test")
