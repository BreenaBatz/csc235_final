from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import _sqlite3
import os, json
from werkzeug.utils import secure_filename


app = Flask(__name__)
 
#database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///meads.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False

db = SQLAlchemy(app)


#Class for the database model for meads, blog posts, events, and stores

class Mead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(120), nullable = False)
    flavor = db.Column(db.String(120), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    alcohol_content = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.Text, nullable = False)
    img = db.Column(db.String(255))
    url = db.Column(db.String(255))
    status = db.Column(db.String(50), default="available") 
    story = db.Column(db.Text, nullable=True) 
    artist = db.Column(db.String(120), nullable=True)
    

    def __repr__(self):
        return f"<Mead {self.name}>"
    
class BlogPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.String(50))
    featured_image = db.Column(db.String(300))   # featured image
    images = db.Column(db.Text)         # NEW: list of extra images


    def __repr__(self):
        return f"<BlogPost {self.title}>"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100))
    location = db.Column(db.String(200))
    def __repr__(self):
        return f"<Event {self.title}>"


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(300))
    city = db.Column(db.String(120))
    zip_code = db.Column(db.String(20))
    def __repr__(self):
        return f"<Store {self.name}>"


#Routes for the website

@app.route("/")
def home(): 
    return render_template("home.html")


#Meads routes
@app.route("/meads")
def meads(): 
    all_meads = Mead.query.all()
    return render_template("meads.html", meads=all_meads)

@app.route("/story/<name>")
def story(name):
    mead = Mead.query.filter_by(name=name).first_or_404()
    return render_template("story.html", mead=mead)


#blog routes
@app.route("/blog")
def blog(): 
    posts = BlogPosts.query.all()
    return render_template("blog.html", posts=posts)


@app.route("/blog/new", methods=["GET", "POST"])
def new_blog_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        date_posted = request.form.get("date") or datetime.now().strftime("%Y-%m-%d")

        # --- FIXED FEATURED IMAGE HANDLING ---
        featured_image_file = request.files.get("image")
        featured_image = None

        if featured_image_file and featured_image_file.filename != "":
            filename = secure_filename(featured_image_file.filename)
            featured_image_file.save(os.path.join("static/blog_images", filename))
            featured_image = filename

        # --- MULTIPLE IMAGES ---
        uploaded_files = request.files.getlist("images")
        saved_images = []

        for file in uploaded_files:
            if file.filename != "":
                filename = secure_filename(file.filename)
                file.save(os.path.join("static/blog_images", filename))
                saved_images.append(filename)

        new_post = BlogPosts(
            title=title,
            content=content,
            date_posted=date_posted,
            featured_image=featured_image,
            images=json.dumps(saved_images)
        )

        db.session.add(new_post)
        db.session.commit()

        return redirect("/blog")

    return render_template("new_blog_post.html")



@app.route("/blog_posts/<int:post_id>")
def blog_post(post_id):
    post = BlogPosts.query.get_or_404(post_id)
    return render_template("blog_post.html", post=post)

#FAQ route

@app.route("/faq")
def faq(): 
    return render_template("faq.html")


#Find Us routes

@app.route("/find_us")
def find_us(): 
    events = Event.query.all()
    stores = Store.query.all()
    return render_template("find_us.html", events=events, stores=stores)

@app.route("/find_us/new", methods=["GET", "POST"])
def new_event():
    if request.method == "POST":
        title = request.form["title"]
        date = request.form["date"]
        time = request.form["time"]
        location = request.form["location"]

        new_event = Event(title=title, date=date, time=time, location=location)
        db.session.add(new_event)
        db.session.commit()

        return redirect("/find_us")

    return render_template("new_upcoming_event.html")




#events route

@app.route("/events")
def events():
    return render_template("events.html")






with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)