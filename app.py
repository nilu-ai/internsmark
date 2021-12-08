from flask import *
from flask.templating import render_template
from flask_mail import Mail, Message
from functools import wraps

import sqlite3
app=Flask(__name__)


app.secret_key = 'super secret key'
mail = Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USERNAME'] = 'marksintern@gmail.com'
app.config['MAIL_PASSWORD'] = 'Nileshraut@12'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/sitemap')
def sit():
    return render_template("sitemap.xml")

@app.route('/Learn_Machine_Learning')
def siast():
    return render_template("ml.html")


@app.route("/edit")

def edit():


    return render_template('edit.html')
@app.route("/edit",methods = ["POST"])
def editecord():
    x='test'
    try:
        sqliteConnection = sqlite3.connect('intern_detials.db')
        quantity=request.form['id2']
        a=request.form['id']
        li=[(quantity,a)]

        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_update_query = """Update Int_info set link = ? where id = ?"""
        cursor.executemany(sqlite_update_query, li)
        sqliteConnection.commit()
        x="Records updated successfully"
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        X="Failed to update multiple records of sqlite table"
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

    return """<script type="text/javascript">
alert("{{ x }}");
</script><a href="/">Go back to home page</a>"""



@app.route('/')
def index():
    connection = sqlite3.connect("intern_detials.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("select * from Int_Info ORDER BY id DESC")
    rows = cursor.fetchall()

    return render_template('index.html',rows=rows)

@app.route('/contact')
def contact():

    return render_template('contact.html')

@app.route("/contact",methods = ["POST"])
def contacts():


    email=request.form["email"]
    name=request.form['name']
    mssg=request.form['msg']
    #htmll="""<h1 style=" font-size: 40px;
     #       font-family: Arial, Helvetica, sans-serif;
     #       background: linear-gradient(to right, #f32170,
       #             #ff6b08, #cf23cf, #eedd44);
       #     -webkit-text-fill-color: transparent;
       #     -webkit-background-clip: text;   text-align: center;margin: 4px; padding-top:13vh ">Welcome and thank you for contacting</h1><br>name+ mssg +"""



    connection = sqlite3.connect("contact.db")
    #connection.row_factory = sqlite3.Row
    #cursor = connection.cursor()
    #cursor.execute("select email from I")

    #rows = cursor.fetchall()
    #flag=False
    #for row in rows:
    #    if(row['email']==email):
    #        flag=False
    #    else:
    #        flag=True
    #if(flag):
    cursor = connection.cursor()
    cursor.execute("select * from I where email=?", (email,))
    rows = cursor.fetchall()
    if  rows == []:

        mg={'msg':mssg,'name':name,'email':email}
        mail.send_message('Confirmation and Contact message from Internmarks ',
                          sender=email,
                          recipients = [email],
                          html=render_template('mail.html',msg=mg)
                          )
        connection = sqlite3.connect("contact.db")
        cursor = connection.cursor()
        flash("Confirmation Message sent Check in Spam Foler if not found")
        cursor.execute("INSERT into I (email) values (?)",(email,))
        connection.commit()

        return render_template('contact.html')

    else:
        flash(" already Registerd")
        return render_template('contact.html')





@app.route("/send/email/<int:id>")

def send(id):
    connection = sqlite3.connect("intern_detials.db")

    cursor = connection.cursor()
    cursor.execute("select * from Int_info where id=?", (id,))
    rows = cursor.fetchall()
    out = [item for t in rows for item in t]
    print(out[1])
    dict={        'title':out[1],        'subtitle':out[2]    ,    'link':out[4],        'des':out[3] ,'hi':id ,'lastdate':out[6],'sti':out[5],'qu':out[7],'req':out[8]  }

    connection = sqlite3.connect("contact.db")

    cursor = connection.cursor()
    cursor.execute("select email from I")
    rowss = cursor.fetchall()
    for ro in rowss:
        mail.send_message('New Internship from MarksIntern: '+out[1],
                              sender=ro[0],
                              recipients = [ro[0],],
                              html=render_template('mail2.html',post=dict)
                              )

    return redirect("/")




@app.route('/about_us')
def about():
    return render_template('about.html')


def check_auth(username, password):

    return username == 'Nilesh@12' and password == 'Password!@#$%^&*()_'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/download')
@requires_auth
def downloadFile1():

    path = "contact.db"
    return send_file(path, as_attachment=True)

@app.route('/add')
@requires_auth
def add():
    return render_template('addpost.html')
@app.route('/asdfghjkl')
def addsss():
    return render_template('asdfghjkl.html')

@app.route("/asdfghjkl",methods = ["POST"])
def consssasd():
    ids="Admin@12"
    pas="Password"
    id=request.form["id"]
    passs=request.form["pass"]
    if(id==ids and pas==passs):
        return render_template('addpost.html')
    return render_template('index.html')
@app.route('/deleterecord')
@requires_auth
def rem():
    return render_template('remove.html')
@app.route("/deleterecord",methods = ["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("intern_detials.db") as connection:

        cursor = connection.cursor()
        cursor.execute("select * from Int_Info where id=?", (id,))
        rows = cursor.fetchall()
        if not rows == []:

            cursor.execute("delete from Int_info where id = ?",(id,))
            msg = "Student detial successfully deleted"
            return render_template('success_record.html')

        else:
            msg = "can't be deleted"
            return ('not done')
@app.route("/add",methods = ["POST"])
def cons():
    msg = "msg"


    if request.method == "POST":
        try:
            title=request.form["title"]
            subtitle=request.form["subtitle"]
            des=request.form["des"]

            link=request.form["link"]
            sti=request.form["sti"]
            ldate=request.form["ld"]
            qu=request.form['qu']
            req=request.form['req']


            with sqlite3.connect("intern_detials.db") as connection:

                cursor = connection.cursor()

                cursor.execute("INSERT into Int_info (title,subtitle,des,link,stipend,lastdate,qu,req) values (?,?,?,?,?,?,?,?)",(title,subtitle,des,link,sti,ldate,qu,req))
                connection.commit()
                msg = "Student detials successfully Added"
        except:
            connection = sqlite3.connect("/intern_detials.db")
            connection.rollback()
            msg = "We can not add Student detials to the database"
        finally:
            return render_template("success_record.html",msg = msg)





@app.route('/post/<int:id>')
def post(id):

    connection = sqlite3.connect("intern_detials.db")

    cursor = connection.cursor()
    cursor.execute("select * from Int_info where id=?", (id,))
    rows = cursor.fetchall()
    out = [item for t in rows for item in t]
    print(out[1])
    dict={        'title':out[1],        'subtitle':out[2]    ,    'link':out[4],        'des':out[3] ,'hi':id ,'lastdate':out[6],'sti':out[5],'qu':out[7],'req':out[8]  }
    return render_template('post.html', post=dict)
if __name__=='__main__':
    app.run(debug=True)
