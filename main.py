import string
from replit import db
from flask import Flask, render_template, redirect, request
from flask_cors import CORS
import uuid
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(
  app
)  #This is simple, makes it work, but is basically begging for an XSS attack. Secure or tell them we would secure it later
#make it a ctf problem lmao
ok_chars = string.ascii_letters + string.digits

@app.route('/')  # What happens when the user visits the site
def base_page():
  return render_template('main.html', )


@app.route('/listings')
def listings():
  return render_template('listings.html', )


@app.route('/ping')
def page_3():
  return "pong"


@app.route('/sell', methods=['POST'])
def createlisting():
  return render_template("sell.html")


@app.route("/create", methods=['POST'])
def create():
  pagename = request.form["Name"]
  price = request.form["Price"]
  description = request.form["Desc"]
  info = request.form["Info"]
  if ("images" in request.files):
    file = request.files["fileToUpload"]
    filename=file.filename
    targetPath = "uploads/" + filename
    file.save(targetPath)
    print("fr")
  datathing = [price, description, info]
  try:
    f = open(
      "/home/runner/traysbud9bab9usdbackend/templates/" + pagename + ".html",
      "x")
    html_template = f"""
			<html>
			<head>
				<title>Buyzy - Buy Easy</title>
				<link rel="stylesheet" type="text/css"            href="/static/styles.css"/>
			</head>    
			<body>
				<header>
      <div id="navbar">
        <nav>
          <ul>
            <li><img src="/static/LOGO.png" width="50" height="50"></li>
            <li><a href="https://traysbud9bab9usdbackend.totoeevee.repl.co/#">Home</a></li>
            <li><a href="sell">Sell</a></li>
            <li><a href="listings">Listings</a></li>
          </ul>
        </nav>
      </div>
    </header>
    <div id='information'>
      <br>
			<h1><center><b>{pagename}</b></center></h1>
			<h1>Price: ${price}</h1>
			<h2>{description}</h2>
			<h3>To buy contact: {info}</h3>
   		</div>
			</body>
			</html>
			"""
    f.write(html_template)
    f.close()
    db[pagename] = datathing
    g = open("/home/runner/traysbud9bab9usdbackend/templates/listings.html",
             "a")
    htmla = f"""
		<div id = "listing">
		<header id = '{pagename}'>
		<h2><a href = "https://traysbud9bab9usdbackend.totoeevee.repl.co/{pagename}">{pagename}</a></h2>
		<h3>${price}</h3>
		</header>
		</div>
		<br>"""
    g.write(htmla)
    print("appended")
    g.close()
    return redirect("/" + pagename, code=302)
  except:
    return redirect("/" + pagename, code=302)


@app.route('/<page>')
def show_user_profile(page):
  try:
    return render_template(page + ".html")
  except:
    return 'The page %s does not exist' % page


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)
