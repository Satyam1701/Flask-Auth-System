from flask import Flask,request,render_template,redirect,url_for
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt



app=Flask(__name__)

app.secret_key="4949asdkhdbcjjcddjnsknksx"


app.config['MYSQL_HOST']= "localhost"
app.config['MYSQL_USER']= "root"
app.config['MYSQL_PASSWORD']= "1234"
app.config['MYSQL_DB']= "flask_database"


mysql=MySQL(app)
login_manage= LoginManager()
login_manage.init_app(app)
bcrypt=Bcrypt(app)



#userloaderfunction
@login_manage.user_loader
def load_user(user_id):
    return User.get(user_id)

class User(UserMixin):
    def __init__(self,user_id,name,email):
        self.id = user_id
        self.name = name
        self.email = email
        


    @staticmethod
    def get(user_id):
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT name,email from users where id=%s",(user_id,))
        result=cursor.fetchone()
        cursor.close()
        if result:
            return User(user_id,result[0],result[1])
        

@app.route("/")
def index():
    return("homepage")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
         
       
        email= request.form['email']
        password= request.form['password']

       


        #pass

        cursor=mysql.connection.cursor()
        cursor.execute('SELECT id,name,email,password from users where email=%s',(email,))
        user_data=cursor.fetchone()
        cursor.close()

        if user_data and bcrypt.check_password_hash(user_data[3],password):
            user=User(user_data[0],user_data[1],user_data[2])
            login_user(user)
            return redirect(url_for ('dashboard'))
        #handle login
        #pass

    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        name= request.form['name']
        email= request.form['email']
        password= request.form['password']

        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')


        #pass

        cursor=mysql.connection.cursor()
        cursor.execute('INSERT INTO users (name,email,password) values(%s, %s, %s)',(name,email,hashed_password))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('login'))

        
    return render_template('register.html')

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route("/logout")
def logout():
    logout_user

    return redirect(url_for('login'))



if __name__== '__main__':
    app.run(debug=True)
