import sqlite3
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.app_context().push()
db = sqlite3.connect("C:\\Users\SAGNIK GHOSHAL\Downloads\DB.Browser.for.SQLite-v3.13.1-win64\\Course.db")
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
    return render_template('dashboard.html', courses=courses)
@app.route('/deletedb/<Course_ID>')
def deletedb(Course_ID):
    with sqlite3.connect("upskill_vision.db") as course:
        cursor=course.cursor()
        print(Course_ID,cursor.execute("SELECT * FROM Courses").fetchall())
        cursor.execute("Delete from Courses where (Id)=?",(Course_ID,))
        return redirect(url_for('dashboard'))
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
        return redirect(url_for('dashboard'))
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
        return redirect(url_for('dashboard'))
    return render_template('ui.html')
if __name__ == '__main__':
    app.run(debug=True)
