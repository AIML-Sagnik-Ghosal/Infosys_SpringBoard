import sqlite3
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mail import Mail, Message
app = Flask(__name__)
app.app_context().push()
app.secret_key = "your_secret_key"
db = sqlite3.connect("upskill_vision.db")
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'Sagnik Ghosal'  # Replace with your email
app.config['MAIL_PASSWORD'] = ''  # Use an app password for security
app.config['MAIL_DEFAULT_SENDER'] = ''
mail = Mail(app)
# Routes
@app.route('/')
def index():
    db = sqlite3.connect("upskill_vision.db")
    cursor=db.cursor()
    courses = cursor.execute("SELECT * FROM Courses").fetchall()
    print(courses)
    return render_template('index.html', courses=courses)

@app.route('/dashboard')
def dashboard():
    db = sqlite3.connect("upskill_vision.db")
    cursor=db.cursor()
    courses = cursor.execute("SELECT * FROM Courses").fetchall()
    courses = [[i,cursor.execute("SELECT name FROM users where (id)=?",(i[4],)).fetchone()] for i in courses]
    return render_template('dashboard.html', courses=courses)
@app.route('/deletedb/<Course_ID>')
def deletedb(Course_ID):
    print(Course_ID)
    with sqlite3.connect("upskill_vision.db") as course:
        cursor=course.cursor()
        print(Course_ID,cursor.execute("SELECT * FROM Courses").fetchall())
        cursor.execute("Delete from Courses where (Id)=?",(Course_ID,))
        return redirect(url_for('dashboard'))
def send_email_notification(title, description, duration):
    recipients = ["sghosal2903@gmail.com"]  # Replace with real emails
    subject = f"New Course Added: {title}"
    body = f"""
    Hello,

    A new course has been added!

    📚 Title: {title}
    📖 Description: {description}
    ⏳ Duration: {duration} months

    Please review the course details.

    Regards,
    Course Management System
    """

    try:
        msg = Message(subject, recipients=recipients, body=body)
        mail.send(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
@app.route('/update_course/<Course_ID>', methods=['GET', 'POST'])
def update_course(Course_ID):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        duration = request.form['duration']
        mentor = request.form['mentor']
        with sqlite3.connect("upskill_vision.db") as course:
                cursor=course.cursor()
                cursor.execute("UPDATE Courses set title=?,description=?,duration=?,instructor_id=? where ID=?",(title,description,duration,mentor,Course_ID))
                course.commit()
        flash("Course updated successfully!", "success")
        send_email_notification(title, description, duration)
        db = sqlite3.connect("upskill_vision.db")
        cursor=db.cursor()
        courses = cursor.execute("SELECT * FROM Courses where ID=?",(Course_ID,)).fetchall()
        return render_template('update_course.html',course=courses)
    print(Course_ID)
    db = sqlite3.connect("upskill_vision.db")
    cursor=db.cursor()
    courses = cursor.execute("SELECT * FROM Courses where ID=?",(Course_ID,)).fetchall()
    print(courses)
    return render_template('update_course.html',course=courses)
@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        duration = request.form['duration']
        mentor = request.form['mentor']
        with sqlite3.connect("upskill_vision.db") as course:
            cursor=course.cursor()
            cursor.execute("INSERT INTO courses (title, description,duration,instructor_id) VALUES (?, ?,?,?)", (title, description,duration,mentor))
            course.commit()
        send_email_notification(title, description, duration)
        flash("Course added successfully!", "success")
        return render_template('add_course.html')
    return render_template('add_course.html')
if __name__ == '__main__':
    app.run(debug=True)
