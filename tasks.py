from flask import Flask, render_template,request, redirect
import os
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("DB_NAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

@app.route("/")
def get_tasks():
    tasks = mongo.db.tasks.find()
    return render_template("tasks.html", tasks=tasks)
    
@app.route("/tasks/<collection_name>")
def get_tasks_by_collection(collection_name):
    tasks = mongo.db[collection_name].find()
    return render_template("tasks.html", tasks=tasks)    
    
@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method=="POST":
        form_values = request.form.to_dict()
        form_values["is_urgent"] = "is_urgent" in form_values
        category = form_values["category_name"]
        mongo.db[category].insert_one(form_values)
        return redirect("/")
    else:
        categories = []
        for category in mongo.db.collection_names():
            if not category.startswith("system."):
                categories.append(category)
        
        return render_template("addtask.html", categories=categories)

if __name__ == "__main__":
        app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)