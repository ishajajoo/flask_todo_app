import datetime
from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import abort

app = Flask(__name__, template_folder='template')

client = MongoClient("mongodb+srv://admin:admin@cluster0.mpjrhem.mongodb.net/")

db = client.flask_db
todos = db.todos

@app.route('/', methods = ('GET', 'POST'))
def index():
    if request.method=='POST':
        content = request.form['content']
        desc = request.form['desc']
        degree = request.form['degree']
        time = datetime.datetime.utcnow()
        todos.insert_one({'content': content, 'desc': desc, 'degree': degree, 'date_created': time})
        return redirect(url_for('index'))
    
    all_todos = todos.find()
    return render_template('index.html', all_todos=all_todos)

@app.route('/delete/<id>/')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

@app.route('/update/<id>/', methods = ['GET', 'POST'])
def modify(id):
    if request.method == 'POST':
        content = request.form['content']
        desc = request.form['desc']
        degree = request.form['degree']
        time = datetime.datetime.utcnow()
        todo = todos.find_one({"_id": ObjectId(id)})
        todos.update_one({"_id": ObjectId(id)}, {"$set": {
            "content": content,
            "desc": desc,
            "degree": degree,
            "time": time
        }})

        return redirect("/")
    if request.method == 'GET':
        todo = todos.find_one({"_id": ObjectId(id)})
    return render_template('update.html', todo=todo)


if __name__=="__main__":
    app.run(debug=True, port = 8000)