from flask import Flask, render_template,redirect, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create the Flask app
app = Flask(__name__)
# Configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.secret_key = "Hey this is my secret key"
# Initialize the database object
db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.sno} - {self.title}'


app.app_context().push()

# Define the home route
@app.route('/', methods =['GET', 'POST'])
def home():
    title = None
    if(request.method=='POST'):
        title = request.form['title']
        description = request.form['description']
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
        flash("Added!")
    allTodo = Todo.query.all()
    print(allTodo)
    return render_template('index.html', allTodo = allTodo, todoname = title)

# Define the about route
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if(request.method=='POST'):
        title = request.form['title']
        description = request.form['description']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo = todo) 


@app.route('/delete', methods=['POST'])

def delete():
     todo_id = request.form['id']
     todo = Todo.query.filter_by(sno=todo_id).first()
     if todo:
            db.session.delete(todo)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Todo deleted successfully!'})
     else:
        return jsonify({'success': False, 'message': 'Todo not found!'})
        
 
    

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
