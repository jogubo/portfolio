from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def index():
    categories = Category.query.all()
    return render_template('index.html', categories=categories)


@app.route('/category/<name>')
def category(name):
    category = Category.query.filter_by(name=name).first()
    return render_template('category.html', category=category)


@app.route('/add-category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'GET':
        return render_template('add-category.html')
    elif request.method == 'POST':
        name = request.form.get('name')
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return redirect('/')


# Models
class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return self.name


if __name__ == '__main__':
    app.run()
