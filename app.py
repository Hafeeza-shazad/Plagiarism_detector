from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy  #for communicating with the database without SQL code
from werkzeug.security import check_password_hash
import pickle  #save and load the trained model and tfidf_vectorizer
import random  #for picking tips and memes at random
import pymysql   
pymysql.install_as_MySQLdb()   
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Movienight%401890@127.0.0.1/plagiarism_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # tracking changes made to objects, set to false because uses extra memory
app.config['SECRET_KEY'] = 'my_secret_key'  # For session handling and flash messages
db = SQLAlchemy(app)

model = pickle.load(open('model.pkl','rb'))   #load and open the trained svm model file
tfidf_vectorizer = pickle.load(open('tfidf_vectorizer.pkl','rb'))  #load and open the tfidf_vetcorizer file

# plagiarism prevention tips that will appear when plagiarism is detected 
tips = [
    {"text": "Learn how to paraphrase effectively.", "link": "https://www.uts.edu.au/current-students/support/helps/self-help-resources/academic-skills/how-paraphrase-effectively"},
    {"text": "Types of plagiarism.", "link": "https://www.enago.com/academy/fraud-research-many-types-plagiarism/"},
    {
    "link": "https://www.youtube.com/watch?v=R7WjaIRgO4M",
    "youtube_id": "R7WjaIRgO4M" },
    {"text": "Learn about plagiarism.", "link": "https://www.snhu.edu/about-us/newsroom/education/what-is-considered-plagiarism"},
    {
    "link": "https://www.youtube.com/watch?v=0mF0mFwlnAY",
    "youtube_id": "0mF0mFwlnAY" },
    {"text": "Improve your academic writing skills.", "link": "https://www.unicaf.org/how-to-improve-your-academic-writing-skills/"},
]

class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(100), primary_key=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('Student', 'Instructor', 'Admin'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp()) #stores the current time of when the user was created

class Submission(db.Model):
    __tablename__ = 'submissions'
    submission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(100), db.ForeignKey('users.email'), nullable=False)
    submission_text = db.Column(db.Text, nullable=False)
    submission_date = db.Column(db.TIMESTAMP, default=db.func.current_timestamp()) #stores the current time of submission
    plagiarism_result = db.Column(db.String(50)) 

# Route for the public dashboard
@app.route("/")  # landing page
@app.route("/dashboard")  # Same route for dashboard that is linked in the other pages
def dashboard():
    return render_template('dashboard.html')  


# route: admin dashboard
@app.route("/admin", methods=['GET'])
def admin_dashboard():
    users = User.query.all()  # Fetch all rows from the users table
    return render_template('admin_dashboard.html', users=users)

    
  # Route: Update User Role
@app.route("/admin/update/<string:email>", methods=['POST'])
def update_user(email):
    if 'role' in session and session['role'] == 'Admin':
        user = User.query.filter_by(email=email).first()
        if user:
            new_role = request.form['role']  # Get new role from form
            user.role = new_role
            db.session.commit()
            flash(f"User {user.email}'s role updated to {new_role}.")
        return redirect(url_for('admin_dashboard'))
    else:
        flash("Access Denied. Admins only.")
        return redirect(url_for('dashboard'))


# Route: Delete User
@app.route("/admin/delete/<string:email>", methods=['POST'])
def delete_user(email):
    if 'role' in session and session['role'] == 'Admin':
        user = User.query.filter_by(email=email).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            flash(f"User {user.email} has been deleted.")
        return redirect(url_for('admin_dashboard'))
    else:
        flash("Access Denied. Admins only.")
        return redirect(url_for('dashboard'))
  
       
# Route: User login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Check user credentials
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_email'] = user.email
            session['role'] = user.role
            flash(f"Welcome, {user.email}!")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password.")

    return render_template('login.html') 

@app.route("/index", methods=['GET'])
def index():
    if 'user_email' not in session:
        flash("You must log in to access the plagiarism detector.")
        return redirect(url_for('dashboard'))  # Redirect to the dashboard if not logged in
    
    return render_template('index.html')  # Render the page for plagiarism detection if logged in

# Route: Plagiarism Detection
@app.route("/detect", methods=['POST'])
def detect_plagiarism():
    input_text = request.form['text']
    user_email = session['user_email']

    # Split the text into sentences
    sentences = sent_tokenize(input_text)
    highlighted_text = ""

    # Check each sentence for plagiarism
    plagiarism_detected = False
    for sentence in sentences:
        vectorized_sentence = tfidf_vectorizer.transform([sentence])
        result = model.predict(vectorized_sentence)
        if result[0] == 1:  # Plagiarized
         highlighted_text += f'<span style="background-color: yellow;">{sentence}</span> '
         plagiarism_detected = True
         highlighted_text += sentence + " "  # Always add the sentence to the final text


    # Save the submission to the database
    plagiarism_result = "Plagiarism Detected" if plagiarism_detected else "No Plagiarism Detected"
    new_submission = Submission(user_email=user_email, submission_text=input_text, plagiarism_result=plagiarism_result)
    db.session.add(new_submission)
    db.session.commit()

    if plagiarism_detected:
        # Select 3 random tips
        random.shuffle(tips)
        selected_tips = tips[:3]
        return render_template('index.html', highlighted_text=highlighted_text, result="Plagiarism Detected :(", tips=selected_tips)
    else:
       # List of available meme filenames
        meme_files = ['Plagiarism_Meme1.png', 'Plagiarism_Meme2.png', 'Plagiarism_Meme3.png','Plagiarism_Meme4.png','Plagiarism_Meme5.png','Plagiarism_Meme6.png','Plagiarism_Meme7.png'] 
        
        # Pick a random meme from the list
        random_meme = random.choice(meme_files)
        meme_url = url_for('static', filename=f'images/{random_meme}')  # Generate correct URL for the randomly selected meme
        return render_template('index.html', highlighted_text=highlighted_text, result="No Plagiarism Detected, Good job! :)", meme_url=meme_url)

    
    # Route: User profile
@app.route("/profile", methods=['GET'])
def user_profile():
    # Retrieve the logged-in user's email from the session
    user_email = session['user_email']

    # Fetch user details
    user = User.query.filter_by(email=user_email).first()

    # Fetch user submissions
    submissions = Submission.query.filter_by(user_email=user_email).order_by(Submission.submission_date.desc()).all()

    return render_template('profile.html', user=user, submissions=submissions)



  # Route to handle logout
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('dashboard'))

if __name__=='__main__':
    app.run(debug=True)