from msvcrt import open_osfhandle
from operator import getitem
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta, datetime, timezone
from notify import notify_msg
import time
import random
import threading
import webbrowser
import os; os.getcwd(); os.chdir('D:\학교\\22-1\소프트웨어프로젝트\\termProject')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
app.secret_key="askljd2jkhuisdbkndvcbnkdjkb2jkh2"
db = SQLAlchemy(app)
KTZ = timezone(timedelta(hours=9))
today = date.today() 
alarmTime=""

def getTime():
  global alarmTime
  alarmTime = datetime.now(KTZ).time().strftime("%H:%M:%S")
  threading.Timer(1, getTime).start()

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title=db.Column(db.String(100), nullable=False)
  complete = db.Column(db.Boolean)

class Routin(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  s_date = db.Column(db.DateTime())
  e_date = db.Column(db.DateTime())
  l_date = db.Column(db.Integer)
  title=db.Column(db.String(200), nullable=False)
  duration=db.Column(db.Integer, nullable=False)
  complete = db.Column(db.Boolean)
  per = db.Column(db.Integer)

getTime()

#할 일 part
@app.route('/')
def todos():
  notify = None
  todo_list = Todo.query.all()
  routin_list = Routin.query.all()
  for i in range(1, len(routin_list)+1):
    item=Routin.query.get(i)
    if(datetime.today() <= item.e_date):
        while(alarmTime):
          if("00:00:00"<=alarmTime<"00:01:00" or 
            "09:00:00"<=alarmTime<"09:01:00" or 
            "12:00:00"<=alarmTime<"12:01:00" or 
            "18:00:00"<=alarmTime<"18:01:00" or 
            "22:00:00"<=alarmTime<"22:01:00" or
            "13:38:00"<=alarmTime<"13:40:00"):
            flash("알림을 확인해주세요", "notify")
            notify = notify_msg[random.randrange(0, len(notify_msg))]
            return render_template('home.html', todo_list=todo_list,  
                              routin_list=routin_list,
                              notify = notify)
          else:
            break
    else:
      return render_template('home.html', todo_list=todo_list,routin_list=routin_list)
  return render_template('home.html', todo_list=todo_list, routin_list=routin_list, notify=notify)
  
@app.route("/add", methods=["POST"])
def add():
  title = request.form.get('title')
  new_todo = Todo(title=title, complete=False)
  db.session.add(new_todo)
  db.session.commit()
  return redirect(url_for("todos"))
@app.route("/update/<int:todo_id>")
def update(todo_id):
  todo = Todo.query.filter_by(id=todo_id).first()
  todo.complete= not todo.complete
  db.session.commit()
  return redirect(url_for("todos"))
@app.route("/editing/<int:todo_id>")
def editing(todo_id):
  todo=Todo.query.filter_by(id=todo_id).first()
  routin_list = Routin.query.all()
  for i in range(1, len(routin_list)+1):
    item=Routin.query.get(i)
    if(datetime.today() <= item.e_date):
        while(alarmTime):
          if("00:00:00"<=alarmTime<"00:01:00" or 
            "09:00:00"<=alarmTime<"09:01:00" or 
            "12:00:00"<=alarmTime<"12:01:00" or 
            "18:00:00"<=alarmTime<"18:01:00" or 
            "22:00:00"<=alarmTime<"22:01:00" or
            "13:38:00"<=alarmTime<"13:40:00"):
            flash("알림을 확인해주세요", "notify")
            notify = notify_msg[random.randrange(0, len(notify_msg))]
            return render_template('edit.html', todo=todo, routin_list=routin_list, notify = notify)
          else:
            break
  return render_template('edit.html', todo=todo)
@app.route("/edit/<int:todo_id>", methods=["POST"])
def edit(todo_id):
  editTodo = Todo(title= request.form["title"])
  todo=Todo.query.filter_by(id=todo_id).first()
  todo.title=editTodo.title
  db.session.commit()
  return redirect(url_for("todos"))
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
  todo = Todo.query.filter_by(id=todo_id).first()
  db.session.delete(todo)
  db.session.commit()
  return redirect(url_for("todos"))


#루틴 part
@app.route('/routin')
def routin():
  notify = None
  list = Routin.query.all()
  for i in range(1, len(list)+1):
    item = Routin.query.get(i)
    now=datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
    l_date = (item.e_date-now).days
    item.l_date = l_date+1
    db.session.commit()
    if(datetime.today() >= item.e_date ):
      item.complete = True
      db.session.commit()
  routinList = Routin.query.all()
  for i in range(1, len(list)+1):
    item = Routin.query.get(i)
    if(datetime.today() <= item.e_date):
        while(alarmTime):
          if("00:00:00"<=alarmTime<"00:01:00" or 
            "09:00:00"<=alarmTime<"09:01:00" or 
            "12:00:00"<=alarmTime<"12:01:00" or 
            "18:00:00"<=alarmTime<"18:01:00" or 
            "22:00:00"<=alarmTime<"22:01:00" or
            "13:38:00"<=alarmTime<"13:40:00"):
            flash("알림을 확인해주세요", "notify")
            notify = notify_msg[random.randrange(0, len(notify_msg))]
            return render_template('routin.html', routinList=routinList, notify = notify)
          else:
            break
  return render_template('routin.html', routinList=routinList,  notify = notify)
@app.route("/routin/add", methods=["POST"])
def rAdd():
  title = request.form.get('title')
  duration = request.form.get('duration')
  s_date = date.today()
  p_date = timedelta(days=int(duration))
  e_date = s_date+p_date
  new_routin = Routin(title=title, duration=duration, e_date=e_date, s_date=s_date, complete=False)
  db.session.add(new_routin)
  db.session.commit()
  return redirect(url_for("routin"))
@app.route("/routin/update/<int:routin_id>")
def rUpdate(routin_id):
  routin = Routin.query.filter_by(id=routin_id).first()
  routin.complete= not routin.complete
  db.session.commit()
  return redirect(url_for("routin"))
@app.route("/routin/editing/<int:routin_id>")
def rEditing(routin_id):
  routin=Routin.query.filter_by(id=routin_id).first()
  routin_list = Routin.query.all()
  for i in range(1, len(routin_list)+1):
    item=Routin.query.get(i)
    if(datetime.today() <= item.e_date):
        while(alarmTime):
          if("00:00:00"<=alarmTime<"00:01:00" or 
            "09:00:00"<=alarmTime<"09:01:00" or 
            "12:00:00"<=alarmTime<"12:01:00" or 
            "18:00:00"<=alarmTime<"18:01:00" or 
            "22:00:00"<=alarmTime<"22:01:00" or
            "13:38:00"<=alarmTime<"13:40:00"):
            flash("알림을 확인해주세요", "notify")
            notify = notify_msg[random.randrange(0, len(notify_msg))]
            return render_template('redit.html', routin=routin, routin_list=routin_list, notify = notify)
          else:
            break
  return render_template('redit.html', routin=routin)
@app.route("/routin/edit/<int:routin_id>", methods=["POST"])
def rEdit(routin_id):
  editRoutin = Routin(title= request.form["title"], duration=request.form['duration'])
  routin=Routin.query.filter_by(id=routin_id).first()
  routin.title=editRoutin.title
  routin.duration = editRoutin.duration
  p_date = timedelta(days=int(editRoutin.duration))
  routin.e_date = routin.s_date+p_date
  now=datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
  routin.l_date = (routin.e_date-now).days
  db.session.commit()
  return redirect(url_for("routin"))
@app.route("/routin/delete/<int:routin_id>")
def rDelete(routin_id):
  routin = Routin.query.filter_by(id=routin_id).first()
  db.session.delete(routin)
  db.session.commit()
  return redirect(url_for("routin"))
  
#진행사항 가시화
@app.route('/progress')
def precent():
  notify = None
  list = Routin.query.all()
  for i in range(1, len(list)+1):
    item = Routin.query.get(i)
    item.per = round(((item.duration-item.l_date)/item.duration)*100,2)
    if(item.per >= 100):
      item.per = 100
    if(datetime.today() >= item.e_date):
      item.complete = True
    db.session.commit()
  routinList = Routin.query.all()
  for i in range(1, len(list)+1):
    item=Routin.query.get(i)
    if(datetime.today() <= item.e_date):
        while(alarmTime):
            if("00:00:00"<=alarmTime<"00:01:00" or 
              "09:00:00"<=alarmTime<"09:01:00" or 
              "12:00:00"<=alarmTime<"12:01:00" or 
              "18:00:00"<=alarmTime<"18:01:00" or 
              "22:00:00"<=alarmTime<"22:01:00" or
              "13:38:00"<=alarmTime<"13:40:00"):
              flash("알림을 확인해주세요", "notify")
              notify = notify_msg[random.randrange(0, len(notify_msg))]
              return render_template('progress.html', routinList=routinList, notify = notify)
            else:
              break
  return render_template('progress.html', routinList=routinList, notify = notify)

db.create_all()
port = 5000

if __name__ == "__main__":
  webbrowser.open_new('http://127.0.0.1:'+str(port)+'/')
  app.run(port=port, debug=True)



