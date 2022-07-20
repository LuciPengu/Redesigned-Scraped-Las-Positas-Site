from flask import Flask, render_template
import requests
  
# api-endpoint
URL = "https://gdbackend.hydrabeans.repl.co/getLevel"
  
# location given here
location = "delhi technological university"
  
# defining a params dict for the parameters to be sent to the API
PARAMS = {'address':location}
  
# sending get request and saving the response as response object
r = requests.get(url = URL, params = PARAMS)
  
# extracting data in json format
data = r.json()
print(data)
app = Flask(__name__)

@app.route("/",methods = ["GET"])
def main():
    return render_template("index.html", data=scraper.data)

if __name__ == "__main__":
    app.run(debug=True, host = "0.0.0.0")