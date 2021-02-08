import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
#from tempfile import mkdtemp
#from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from functions import login_required

# Configure application
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL(os.getenv("DATABASE_URL"))

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#FOR VOTE HTML
# <meta http-equiv="refresh" content="5" >

amt = 0

forr = 0
agains = 0
obstain = 0

counter = []
counter1 = []
counter2 = []

final_count = []
final_vote = []

countries = []

# For Hand Raising
number_track = 0
number_hand = []
country_hand = []
type_hand = []

@app.route("/voting", methods=["GET", "POST"])
@login_required

def voting():

    global counter
    global counter1
    global counter2


    options = ["In Favor", "Abstention", "Against"]


    if request.method == "GET":
        return render_template("voting.html", counter = counter, counter1 = counter1, counter2 = counter2, options = options)

    else:

        vote = request.form.get("vote")

        first_country = db.execute("SELECT username FROM accounts WHERE id = :user_id", user_id = session["user_id"])
        country = first_country[0]["username"]

        global countries

        #countries[country] = vote

        inside = False

        """

        for items in countries:
            for things in final_count:
                if things == items:
                    inside = True
                    break
            else:
                inside = False
                final_count.append(items)

        if inside == False:
            for items in countries.values():
                final_vote.append(items)
        """

        #print(countries)
        #print("!!!!!")
        #print(country)
        #print("!!!!!")

        for items in countries:
            if str(items) == str(country):
                x = countries.index(country)
                earlier_vote = final_vote[x]
                final_vote[x] = vote
                inside = True

        if inside == False:
            countries.append(country)

        if inside == True:
            if earlier_vote == "In Favor":
                counter.pop()
            elif earlier_vote == "Abstention":
                counter1.pop()
            elif earlier_vote == "Against":
                counter2.pop()
            if vote == "In Favor":
                counter.append("a")
            elif vote == "Abstention":
                counter1.append("a")
            elif vote == "Against":
                counter2.append("a")




        if inside == False:
            final_count.append(country)
            final_vote.append(vote)

            #print(countries)

                #for items in countries.values():
                 #   final_vote.append(items)s

            global amt
            global forr
            global agains
            global obstain
            global type_hand
            global country_hand
            global number_track

            amt = len(final_vote)


            if vote == "In Favor":
                counter.append("a")
            elif vote == "Abstention":
                counter1.append("a")
            elif vote == "Against":
                counter2.append("a")

        forr = len(counter)
        agains = len(counter2)
        obstain = len(counter1)

        return redirect("/")
@app.route("/", methods=["GET", "POST"])
@login_required
def vot():

    global forr
    global agains
    global obstain
    global type_hand
    global country_hand
    global number_track
    before_country_raise = db.execute("SELECT username FROM accounts WHERE id = :user_id", user_id = session["user_id"])
    current_country = before_country_raise[0]["username"]

    if request.method == "GET":
        if current_country == "Chair":
            return render_template("chair.html", final_count = final_count, final_vote = final_vote, amt = amt, forr = forr, obstain = obstain, agains = agains, country_hand = country_hand, type_hand = type_hand, number_track = number_track)
        else:
            return render_template("vote.html", final_count = final_count, final_vote = final_vote, amt = amt, forr = forr, obstain = obstain, agains = agains, country_hand = country_hand, type_hand = type_hand, number_track = number_track)




@app.route("/login", methods=["GET", "POST"])
def login():








    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("login.html")


    # User reached route via POST (as by submitting a form via POST)
    else:

        #global country
        #country = request.form.get("username"):

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM accounts WHERE username = :username",
                          username=request.form.get("username"))
        #print(rows)

        # Ensure username exists and password is correct
        #if len(rows) != 1:
         #   return redirect("/login")

        #if request.form.get("password") != rows[0]["password"]:
        #    return redirect("/login")
        # Ensure username exists and password is correct
        #y = check_password_hash(rows[0]["password"], request.form.get("password"))
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return render_template("login.html")

        #if rows[0]["password"] != request.form.get("password")):
           # return apology("invalid", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return redirect("/")


@app.route("/chair", methods=["GET", "POST"])
def chair():
    if request.method == "POST":
        global counter
        global counter1
        global counter2
        global final_count
        global final_vote
        global agains
        global forr
        global obstain
        global amt
        counter = []
        counter1 = []
        counter2 = []
        final_count = []
        final_vote = []
        amt = 0
        forr = 0
        agains = 0
        obstain = 0
        return redirect("/")


@app.route("/quickrefresh", methods=["GET", "POST"])
def refresh():
    if request.method == "POST":
        return redirect("/")

@app.route("/raise", methods=["GET", "POST"])
def raise_hand():
    if request.method == "GET":
        return render_template("raise.html")
    elif request.method == "POST":
        global type_hand
        global country_hand
        global number_track
        isit = False
        reason = request.form.get("raise_type")
        before_country_raise = db.execute("SELECT username FROM accounts WHERE id = :user_id", user_id = session["user_id"])
        country_raise = before_country_raise[0]["username"]


        for items in country_hand:
            if str(items) == str(country_raise):
                x = country_hand.index(country_raise)
                earlier_raise = type_hand[x]
                type_hand[x] = reason
                isit = True

        if isit == False:
            country_hand.append(country_raise)
            type_hand.append(reason)
        number_track = len(country_hand)
        return redirect("/")

@app.route("/quickraise", methods=["GET", "POST"])
def quick_raise():
    if request.method == "POST":
        global type_hand
        global country_hand
        global number_track
        #sure = False
        before_country_raise = db.execute("SELECT username FROM accounts WHERE id = :user_id", user_id = session["user_id"])
        current_count = before_country_raise[0]["username"]

        for items in country_hand:
            if str(items) == str(current_count):
                x = country_hand.index(current_count)
                country_hand.pop(x)
                type_hand.pop(x)
                return redirect("/")


        return render_template("raise.html")

@app.route("/alldown", methods=["GET", "POST"])
def quick_close():
    if request.method == "POST":
        global type_hand
        global country_hand
        global number_track
        number_track = 0
        country_hand = []
        type_hand = []
        return redirect("/")








