from flask import Flask,render_template,flash,redirect,url_for,request,session
from flask_bcrypt import generate_password_hash,check_password_hash
from config import User
app = Flask(__name__,static_url_path='/static')
app.secret_key ="ajkjdkfdjfkef"

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/wednesday')
def wed():
    return render_template('wednesday.html')

@app.route('/aboutus')
def about():

    return render_template('aboutus.html')


@app.route('/home')
def house():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template('home.html')

@app.route('/users')
def users():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    users = User.select()
    return render_template("users.html", users = users)

@app.route('/delete/<int:id>')
def delete(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    User.delete().where(User.id == id).execute()
    flash("User deleted successfully")
    return redirect(url_for("users"))




@app.route('/update/<int:id>' ,methods=['GET','POST'])
def update(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    user = User.get(User.id == id)
    if request.method =="POST":
        updatedName = request.form["u_name"]
        updatedEmail = request.form["u_email"]
        updatedPassword = request.form["u_pass"]
        user.name = updatedName
        user.email = updatedEmail
        user.password = generate_password_hash(updatedPassword)
        user.save()
        flash("User updated successfully")
        return redirect(url_for("users"))
    return render_template("update.html", user = user)



@app.route('/login' ,methods=['GET','POST'])
def login():
    if request.method == "POST":
        name = request.form["u_name"]
        email = request.form["u_email"]
        password = request.form["u_pass"]
        try:
            user = User.get(User.name == name)
            user = User.get(User.email == email)
            hashed_password = user.password
            if check_password_hash(hashed_password,password):
                flash("Login successful!!!")
                session["logged_in"] = True
                session["name"] = user.name
                return redirect(url_for("house"))
            else:
                flash("Wrong username or password")
        except:
            flash("This operation is not permitted at this time")

    return render_template("Login.html")

if __name__ == '__main__':
    app.run(debug=True)
