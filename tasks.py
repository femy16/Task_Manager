from flask import Flask,render_template
import os
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_DBNAME"]=os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"]=os.environ.get("MONGO_URI")

mongo=PyMongo(app)

@app.route("/")
def show_hi():
    tasks=mongo.db.tasks.find()
    return render_template("tasks.html",tasks=tasks)

if __name__ == "__main__":
        app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)