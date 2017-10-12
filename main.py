from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
blogs = ""

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Blog %r>' % self.title

def get_blogs():
    return Blog.query.all()

#@app.route('/', methods=['POST', 'GET'])
#def index():

@app.route("/")
def index():
    encoded_error = request.args.get("error")
    return render_template('newpost.html', blogs=get_blogs(),error=encoded_error and cgi.escape(encoded_error, quote=True))

#    if request.method == 'POST':
#        blog_name = request.form['name']
#        blog_title = request.form['title']
#        blog_body = request.form['body']
#        new_blog = Blog(blog_name,blog_title,blog_body)
#        db.session.add(new_blog)
#        db.session.commit()
#    return render_template('blogs.html',title="My Blogs!", 
#        blogs=get_blogs())


@app.route("/add", methods=['POST'])
def add_blog():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']

    if len(blog_title) == 0:
        error = "Please enter the title of the blog post."
        return redirect("/?error=" + error)

    if len(blog_body) == 0:
        error = "Please complete the body of the blog post."
        return redirect("/?error=" + error )


    new_blog = Blog(blog_title,blog_body)
    db.session.add(new_blog)
    db.session.commit()
    
    return render_template('blog.html', blogs=get_blogs())


#@app.route('/delete-task', methods=['POST'])
#def delete_task():
#
#    task_id = int(request.form['task-id'])
#    task = Task.query.get(task_id)
#    task.completed = True
#    db.session.add(task)
#    db.session.commit()
#
#    return redirect('/')

@app.route('/blog')
def blog():
    return render_template('blog.html',title="My Blogs!", blogs=get_blogs())

if __name__ == '__main__':
    app.run()