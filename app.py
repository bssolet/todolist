from flask import Flask, render_template,redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create the Flask app
app = Flask(__name__)
# Configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
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
    if(request.method=='POST'):
        title = request.form['title']
        description = request.form['description']
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    print(allTodo)
    return render_template('index.html', allTodo = allTodo)

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


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')   

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
