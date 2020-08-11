from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.models import Sneakers, Article, Category
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    return redirect("/add_snkrs")


@app.route('/add_snkrs', methods=["GET", "POST"])
def add_snkrs():
    if request.method == "POST":
        brand = request.form["brand"]
        model = request.form["model"]
        year = request.form["year"]
        s = Sneakers(brand=brand, model=model, release_year=year)
        print(s)
        db.session.add(s)
        db.session.commit()
        return redirect("/all_snkrs")
    else:
        return render_template("add_snkrs.html")


@app.route('/all_snkrs', methods=["GET"])
def all_snkrs():
    year_start = request.args.get("year_start") or 1950
    year_finish = request.args.get("year_finish") or 2020
    print(year_start, year_finish)
    s = Sneakers.query.filter(Sneakers.release_year >= year_start, Sneakers.release_year <= year_finish)
    print(s)
    return render_template("all_snkrs.html", s=s)


@app.route('/nike_snkrs', methods=["GET"])
def nike_snkrs():
    s = Sneakers.query.filter_by(brand="Nike")
    print(s)
    return render_template("all_snkrs.html", s=s)


@app.route('/twentyk_snkrs', methods=["GET"])
def twentyk_snkrs():
    s = Sneakers.query.filter(Sneakers.release_year >= 2000)
    print(s)
    return render_template("all_snkrs.html", s=s)


@app.route('/add_article', methods=["GET", "POST"])
def add_article():
    if request.method == "POST":
        title = request.form["title"]
        text = request.form["text"]
        category = request.form["category"]
        print(1)
        c = Category.query.filter(Category.name == category).first()
        print(2)
        if not c:
            c = Category(name=category)
        a = Article(title=title, text=text, pub_time=datetime.utcnow(), category=c)
        print(3)
        db.session.add(c)
        db.session.add(a)
        db.session.commit()
        return redirect("/all_articles")
    else:
        return render_template("add_article.html")


@app.route('/all_articles', methods=["GET", "POST"])
def all_articles():
    a = Article.query.all()
    return render_template("all_articles.html", a=a)


@app.route('/sizes', methods=["GET", "POST"])
def sizes():
    if request.method == "POST":
        number = request.form["number"]
        size_type = request.form["size_type"]
        sizes = [
            [6.5, 38.5, 37.5],
            [7, 39, 38],
        ]
        US = 0
        EU = 1
        RU = 2
        if size_type == "us":
            for i in sizes:
                if i[US] == float(number):
                    us_size = i[US]
                    eu_size = i[EU]
                    ru_size = i[RU]
        if size_type == "eu":
            for i in sizes:
                if i[EU] == float(number):
                    us_size = i[US]
                    eu_size = i[EU]
                    ru_size = i[RU]
        if size_type == "ru":
            for i in sizes:
                if i[RU] == float(number):
                    us_size = i[US]
                    eu_size = i[EU]
                    ru_size = i[RU]
        return render_template("filled_sizes.html", us_size=us_size, eu_size=eu_size, ru_size=ru_size)
    else:
        return render_template("sizes.html")
