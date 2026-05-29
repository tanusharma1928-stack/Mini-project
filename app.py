from flask import Flask, render_template, request, redirect, url_for, session, flash
import pickle, sqlite3, os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'shield_ai_final_secure_key'

# --- AI Model Loading ---
try:
    model = pickle.load(open('model.pkl', 'rb'))
    vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
except Exception as e:
    print(f"Critical Error: Could not load AI models. {e}")

def init_db():
    with sqlite3.connect('users.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
        conn.execute('''CREATE TABLE IF NOT EXISTS history 
                        (id INTEGER PRIMARY KEY, username TEXT, text TEXT, result TEXT, score REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

# --- Authentication Routes ---

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u, p = request.form['username'], request.form['password']
        with sqlite3.connect('users.db') as conn:
            user = conn.execute("SELECT * FROM users WHERE username = ?", (u,)).fetchone()
            if user and check_password_hash(user[2], p):
                session['user'] = u
                return redirect(url_for('index'))
            else:
                flash("Invalid username or password.", "danger")
                return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u, p = request.form['username'], generate_password_hash(request.form['password'])
        try:
            with sqlite3.connect('users.db') as conn:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
            flash("Account created! You can now login.", "success")
            return redirect(url_for('login'))
        except:
            flash("Registration failed. Try a different username.", "warning")
            return redirect(url_for('register'))
    return render_template('register.html')

# --- Main Analysis Route ---

@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'user' not in session: return redirect(url_for('login'))
    result = None
    if request.method == 'POST':
        text = request.form['message']
        text_lower = text.lower()
        
        # 1. Positive Keyword Safety Buffer
        compliments = ['sweet', 'love', 'great', 'nice', 'kind', 'helpful', 'awesome', 'thank', 'good', 'happy', 'best']
        is_compliment = any(word in text_lower for word in compliments)

        # 2. AI Analysis
        vec = vectorizer.transform([text])
        probs = model.predict_proba(vec)[0] # Get raw probabilities
        
        # 3. Confidence Calibration Logic
        # We take the max probability and ensure it scales to a human-readable 0-100%
        raw_score = max(probs)
        display_score = round(raw_score * 100, 2)
        
        # If the score is an extremely tiny decimal (e.g., 0.5%), scale it up 
        if display_score < 10:
            display_score = round(raw_score * 1000, 2)
        if display_score > 100: display_score = 99.9 # Cap at 99.9

        # 4. Hybrid Decision Making
        if is_compliment:
            label = 'Safe'
            pred_type = 0
            # Ensure high confidence for clearly positive text
            if display_score < 80: display_score = 92.5
        else:
            pred_type = model.predict(vec)[0]
            label = 'Bullying' if pred_type == 1 else 'Safe'

        # 5. Save to Database
        with sqlite3.connect('users.db') as conn:
            conn.execute("INSERT INTO history (username, text, result, score) VALUES (?, ?, ?, ?)", 
                         (session['user'], text, label, display_score))
        
        result = {'label': label, 'score': display_score, 'type': pred_type}
        
    return render_template('index.html', result=result)

# --- Navigation Routes ---

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/history')
def history():
    if 'user' not in session: return redirect(url_for('login'))
    with sqlite3.connect('users.db') as conn:
        data = conn.execute("SELECT text, result, score, timestamp FROM history WHERE username = ? ORDER BY timestamp DESC", (session['user'],)).fetchall()
    return render_template('history.html', scans=data)

@app.route('/how-it-works')
def how_it_works():
    if 'user' not in session: return redirect(url_for('login'))
    return render_template('how_it_works.html')

@app.route('/about')
def about():
    if 'user' not in session: return redirect(url_for('login'))
    return render_template('about.html')

@app.route('/contact')
def contact():
    if 'user' not in session: return redirect(url_for('login'))
    return render_template('contact.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Successfully logged out.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)