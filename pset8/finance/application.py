import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, checksymbol

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "GET":
        # get username and cash amount from table users
        rows = db.execute("SELECT username, cash FROM users WHERE id = :id", id=session["user_id"])
        cash = rows[0]["cash"]
        cashFormatted = usd(rows[0]["cash"])
        username = rows[0]["username"]

        # get stocks from table purchases
        purchases = db.execute("SELECT symbol, shares FROM purchases WHERE username = :username ORDER BY symbol", username=username)

        totalforAllStock = 0

        # add current price and total of purchases to the dictionary
        for i in range(len(purchases)):
            symbol = purchases[i]["symbol"]
            lookupresult = lookup(symbol)
            price = lookupresult["price"]
            purchases[i]["price"] = price
            purchases[i]["priceFormatted"] = usd(price)
            purchases[i]["totalForStockFormatted"] = usd(price* int(purchases[i]["shares"]))
            purchases[i]["totalForStock"] = price*int(purchases[i]["shares"])

            totalforAllStock += purchases[i]["totalForStock"]

        # calculate the total (cash + stock's total)
        totalCashAndStock = cash + totalforAllStock
        totalCashAndStockFormatted = usd(totalCashAndStock)

        return render_template("portfolio.html", cash=cashFormatted, username=username, portfolio=purchases, gross=totalCashAndStockFormatted)



    """Add cash to user's account"""
    if request.method == "POST":

        cash = int(request.form.get("addcash"))

        if cash < 1:
            return apology("must provide a positive number", 400)
        else:
            rows = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
            cashBefore = rows[0]["cash"]
            newAmount = cash + cashBefore
            db.execute("UPDATE users SET cash = (:cash) WHERE id = :id", cash=newAmount, id=session["user_id"])

            # Redirect user to home page
            return redirect("/")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
        # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("symbol") or not request.form.get("shares"):
            return apology("must provide symbol and shares", 400)
        if int(request.form.get("shares")) < 1:
            return apology("must provide a positive number", 400)
        symbol = request.form.get("symbol")
        resultquote = lookup(symbol)

        if resultquote:
            price = resultquote["price"]
            shares = request.form.get("shares")

            # Query database for amount of cash the user has
            rows = db.execute("SELECT cash FROM users WHERE id = :id",
                          id=session["user_id"])
            cash = rows[0]["cash"]
            total = price * int(shares)

            # Allow purchase if user has enough $
            if cash >= total:
                rows = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
                username=rows[0]["username"]
                company = resultquote["name"]
                shares = int(shares)

                db.execute("INSERT INTO purchases (username, company, price, shares, symbol, total) VALUES (:username, :company, :price, :shares, :symbol, :total)",
                username=username, company=company, price=price, shares=shares, symbol=symbol, total=total)

                # Update amount of cash remaning for the user
                newAmount = cash - total
                db.execute("UPDATE users SET cash = (:cash) WHERE id = :id", cash=newAmount, id=session["user_id"])

            else:
                return apology("you don't have enough cash")

            # Redirect user to home page
            return redirect("/")

        else:
            return apology("must provide a valid symbol", 400)

    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # get the parameter from the url (?username=value)
    username = request.args.get('username')

    # get usernames existing in the DB
    rows = db.execute("SELECT username FROM users WHERE username = :username", username=username)
    print(rows)
    # return true if the value of username is of length at least 1 and does not already belong to a user in the DB
    if len(username) > 0 and len(rows) < 1:
        print('true', len(rows))
        return jsonify(True)
    else:
        return jsonify(False)
    return render_template("login.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    if request.method == "GET":
        # get username and cash amount from table users
        rows = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
        username = rows[0]["username"]

        # get stocks from table purchases
        purchases = db.execute("SELECT symbol, shares, time, price FROM purchases WHERE username = :username ORDER BY time", username=username)

        # add current price and format price of purchase
        for i in range(len(purchases)):
            symbol = purchases[i]["symbol"]
            lookupresult = lookup(symbol)
            priceNow = lookupresult["price"]
            purchases[i]["priceNow"] = usd(priceNow)
            purchases[i]["price"] = usd(purchases[i]["price"])
            # add column saying if sale purchase
            if purchases[i]["shares"] < 0 :
                purchases[i]["transaction"] = "Sale"
            else:
                purchases[i]["transaction"] = "Purchase"

        return render_template("history.html", username=username, portfolio=purchases)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        symbol = request.form.get("symbol")
        resultquote = lookup(symbol)
        if resultquote:
            return render_template("quoted.html", quote=resultquote)
        else:
            return apology("must provide a valid symbol", 400)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide a password confirmation", 400)

        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("the two passwords do not match :/", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        if rows :
            return apology("this username already exists", 400)

        # Insert user into the DB
        hash = generate_password_hash(request.form.get("password"))
        rows = db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=request.form.get("username"), password=hash)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # get list of the existing symbols
    symbols = checksymbol()

    if request.method == "POST":

        # check if user choose a stock correctly and if he owns shares of that stock
        rows = db.execute("SELECT username, cash FROM users WHERE id = :id", id=session["user_id"])
        username = rows[0]["username"]
        rows1 = db.execute("SELECT symbol, shares FROM purchases WHERE username = :username", username=username)

        chosenSymbol = request.form.get("symbol")
        sharesToSell = int(request.form.get("shares"))
        owned = 0

        for i in range(len(rows1)):
            if rows1[i]["symbol"] == chosenSymbol:
                # get amount of shares in one particular purchase
                amountFromThisPurchase = rows1[i]["shares"]
                # addition of all the shares from the different purchases
                owned = owned + amountFromThisPurchase

        if not chosenSymbol or owned < sharesToSell:
            return apology("not enough of this stock", 400)

        if sharesToSell < 1:
            return apology("must provide a positive number", 400)

        lookupresult = lookup(chosenSymbol)
        price = lookupresult["price"]
        company = lookupresult["name"]

        totalSold = price * sharesToSell

        sharesToSell = -sharesToSell

        rows2 = db.execute("INSERT INTO purchases (username, company, price, shares, symbol, total) VALUES (:username, :company, :price, :shares, :symbol, :total)",
                username=username, company=company, price=price, shares=sharesToSell, symbol=chosenSymbol, total=totalSold)

        # Query database for amount of cash the user has
        rowsCash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        cash = rowsCash[0]["cash"]

        # Update amount of cash remaning for the user
        newAmount = cash + totalSold
        db.execute("UPDATE users SET cash = (:cash) WHERE id = :id", cash=newAmount, id=session["user_id"])

        return redirect("/")

    return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
