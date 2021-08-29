from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]="sqlite:///todo.db"

db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    desc=db.Column(db.String(100),nullable=True)
    date=db.Column(db.DateTime,default=datetime.utcnow())

    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}" #to diplay beautifully when we use print 

@app.route("/",methods=["POST","GET"])
def home():
    if request.method=="POST":
        # print(request.form["title"])
        # print(request.form["message"])
        title=request.form["title"]
        content=request.form["content"]
        todo=Todo(title=title,desc=content)
        db.session.add(todo)
        db.session.commit()
    alltodo=Todo.query.all()
    return render_template("index.html",alltodo=alltodo)

@app.route("/update/<int:sno>",methods=["GET","POST"])
def update(sno):
    if request.method=="POST":
        title=request.form["title"]
        content=request.form["content"]
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=content
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo)



@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return  redirect("/")#to redirect user to the home page


if __name__=="__main__":
    app.run(debug=True)#debug=True it will give us error in html page if occurs. Dont use it in working server.Use for development purpose only.