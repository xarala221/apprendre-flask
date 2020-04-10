from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy  # add
from datetime import datetime  # add

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # add
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # add


# add
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    done = db.Column(db.Boolean, unique=False, default=True)

    def __repr__(self):
        return '<Todo %r>' % self.name


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['task']
        new_task = Task(name=name)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception:
            return "Une erreur s'est produite."

    else:
        tasks = Task.query.filter(Task.done).order_by(Task.created_at)
        return render_template('index.html', tasks=tasks)


@app.route("/about/")
def about():
    return render_template("about.html")

# supprimer une tache
@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except Exception:
        return "There was a problem deleting data."
# update
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Task.query.get_or_404(id)

    if request.method == 'POST':
        task.name = request.form['name']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating data."

    else:
        title = "Update Data"
        return render_template('update.html', title=title, task=task)


if __name__ == '__main__':
    app.run(debug=True)
