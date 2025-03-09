import sqlite3
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mail import Mail, Message
import json
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
app.config['MAIL_DEFAULT_SENDER'] = 'noobengineer20@gmail.com'
New_Courses=[]
mail = Mail(app)
def insert_quiz_question(question_text, course_id, options_json, answer, points):
    conn = sqlite3.connect("upskill_vision.db")
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO quiz(question_text,course_id, options, correct_answer, points)
    VALUES (?, ?, ?,?, ?)
    ''', (question_text, course_id, options_json, answer, points))
    
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def index():
    db = sqlite3.connect("upskill_vision.db")
    cursor=db.cursor()
    courses = cursor.execute("SELECT * FROM Courses").fetchall()
    return render_template('index.html', courses=courses)

@app.route('/dashboard')
def dashboard():
    global New_Courses
    New_Courses=[]
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
        cursor.execute("Delete from Courses where (Id)=?",(Course_ID,))
        cursor.execute("Delete from Module where (Course_Id)=?",(Course_ID,))
        cursor.execute("Delete from Quiz where (Course_Id)=?",(Course_ID,))
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
        image = request.form['image']
        with sqlite3.connect("upskill_vision.db") as course:
                cursor=course.cursor()
                cursor.execute("UPDATE Courses set title=?,description=?,duration=?,instructor_id=?,images=? where ID=?",(title,description,duration,mentor,image,Course_ID))
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
    return render_template('update_course.html',course=courses)
@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        duration = request.form['duration']
        mentor = request.form['mentor']
        image = request.form['image']
        with sqlite3.connect("upskill_vision.db") as course:
            cursor=course.cursor()
            cursor.execute("INSERT INTO courses (title, description,duration,instructor_id,images) VALUES (?, ?,?,?,?)", (title, description,duration,mentor,image))
            course.commit()
        send_email_notification(title, description, duration)
        flash("Course added successfully!", "success")
        db = sqlite3.connect("upskill_vision.db")
        cursor=db.cursor()
        id = cursor.execute("SELECT max(id) FROM Courses").fetchone()
        global New_Courses
        New_Courses.append([id[0],title])
        print(New_Courses)
        return render_template('add_course.html')
    return render_template('add_course.html')
@app.route('/update_module/<Module_ID>', methods=['GET', 'POST'])
def update_module(Module_ID):
    if request.method == 'POST':
        Course_ID= request.form['course_id']
        title = request.form['title']
        content = request.form['content']
        learning_points = request.form['learning_points']
        with sqlite3.connect("upskill_vision.db") as course:
            cursor=course.cursor()
            print((1,title, content,learning_points))
            cursor.execute("INSERT INTO module (course_id,title, content,learning_points) VALUES (?, ?,?,?)", (Course_ID,title, content,learning_points))
            course.commit()
        #send_email_notification(title, description, duration)
        flash("Module added successfully!", "success")
        return render_template('add_module.html',courses=New_Courses)
    print(Module_ID)
    db = sqlite3.connect("upskill_vision.db")
    cursor=db.cursor()
    module = cursor.execute("SELECT * FROM Module where ID=?",(Module_ID,)).fetchall()
    return render_template('update_course.html',course=module)
@app.route('/add_module', methods=['GET', 'POST'])
def add_module():
    global New_Courses
    print(New_Courses)
    if request.method == 'POST':
        Course_ID= request.form['course_id']
        title = request.form['title']
        content = request.form['content']
        learning_points = request.form['learning_points']
        with sqlite3.connect("upskill_vision.db") as course:
            cursor=course.cursor()
            module_no = cursor.execute("SELECT max(module_no) FROM Module group by Course_ID having Course_ID=?",(Course_ID,)).fetchall()
            print(module_no)
            if module_no==[]:
                module_no=1
            else:
                module_no=module_no[0][0]+1
            cursor.execute("INSERT INTO module (course_id,title, content,learning_points,module_no) VALUES (?, ?,?,?,?)", (Course_ID,title, content,learning_points,module_no))
            course.commit()
        #send_email_notification(title, description, duration)
        flash("Module added successfully!", "success")
        return render_template('add_module.html',courses=New_Courses)
    return render_template('add_module.html',courses=New_Courses)
@app.route('/update_question/<Course_ID>/<question_no>', methods=['GET', 'POST'])
def update_question(Course_ID,question_no):
    if request.method == 'POST':
        question_text = request.form['question_text']
        course_id=request.form['course_id']
        options_json = request.form.getlist('options[]')  
        answer = request.form['answer']
        points = request.form['points']
        with sqlite3.connect("upskill_vision.db") as course:
                cursor=course.cursor()
                cursor.execute("UPDATE Courses set question_text=?,course_id=?, options=?, correct_answer=?, points=? where ID=?",(question_text, course_id, options_json, answer, points, Course_ID))
                course.commit()
        flash("Course updated successfully!", "success")
        #send_email_notification(title, description, duration)
        db = sqlite3.connect("upskill_vision.db")
        cursor=db.cursor()
        questions = cursor.execute("SELECT ID FROM Quiz where Course_ID=?",(Course_ID,)).fetchall()
        question = cursor.execute("SELECT * FROM Quiz where ID=?",(questions[question_no],)).fetchall()
        return render_template('update_question.html',question=question)
    print(Course_ID)
    db = sqlite3.connect("upskill_vision.db")
    cursor=db.cursor()
    courses = cursor.execute("SELECT * FROM Courses where ID=?",(Course_ID,)).fetchall()
    return render_template('update_course.html',course=courses)
@app.route('/add_questions', methods=['GET', 'POST'])
def add_question():
    global New_Courses
    print(New_Courses)
    if request.method == 'POST':        
        question_text = request.form['question_text']
        course_id=request.form['course_id']
        options = request.form.getlist('options[]')  
        answer = request.form['answer']
        points = request.fosrm['points']
        options_json = json.dumps({"options": [{"id": chr(65 + i), "text": opt} for i, opt in enumerate(options)]})
        insert_quiz_question(question_text, course_id, options_json, answer, points)
        return render_template('add_question.html', courses=New_Courses, current=['',''])

    return render_template('add_question.html', courses=New_Courses,current=['',''])
if __name__ == '__main__':
    app.run(debug=True)