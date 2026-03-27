from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/aboutus")
def aboutus():
    return render_template("About_Us.html")

@app.route("/getstarted")
def getstarted():
    return render_template("Get_Started.html")



@app.route("/contactus")
def contactus():
    return render_template("Contact_Us.html")

@app.route("/checkout")
def checkout():
    return render_template("Checkout.html")


app.run(debug=True)


