from flask import Flask, render_template, request, redirect, url_for, session
from database import get_db_connection, init_db

app = Flask(__name__)
app.secret_key = 'auspify_exam_secret_key'
init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    results = conn.execute('SELECT * FROM results ORDER BY id DESC').fetchall()
    total_exams = len(results)
    avg_score = sum(r['percentage'] for r in results) / total_exams if total_exams > 0 else 0
    conn.close()
    return render_template('index.html', results=results, total_exams=total_exams, avg_score=round(avg_score, 2))

@app.route('/start_exam', methods=['POST'])
def start_exam():
    username = request.form.get('username').strip()
    email = request.form.get('email').strip()
    if not username or not email:
        return redirect(url_for('index'))
    
    session['username'] = username
    conn = get_db_connection()
    try:
        conn.execute('INSERT OR IGNORE INTO users (username, email) VALUES (?, ?)', (username, email))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()
        
    return redirect(url_for('take_exam'))

@app.route('/exam')
def take_exam():
    if 'username' not in session:
        return redirect(url_for('index'))
    conn = get_db_connection()
    questions = conn.execute('SELECT * FROM questions').fetchall()
    conn.close()
    return render_template('exam.html', questions=questions, username=session['username'])

@app.route('/submit_exam', methods=['POST'])
def submit_exam():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    username = session['username']
    conn = get_db_connection()
    questions = conn.execute('SELECT * FROM questions').fetchall()
    
    score = 0
    total = len(questions)
    
    for q in questions:
        q_id = str(q['id'])
        user_answer = request.form.get(f'q_{q_id}')
        if user_answer and user_answer.strip() == q['correct_option'].strip():
            score += 1
            
    percentage = (score / total) * 100 if total > 0 else 0
    status = 'Pass' if percentage >= 50 else 'Fail'
    
    conn.execute('INSERT INTO results (username, score, total, percentage, status) VALUES (?, ?, ?, ?, ?)',
                 (username, score, total, percentage, status))
    conn.commit()
    conn.close()
    
    return render_template('result.html', username=username, score=score, total=total, percentage=percentage, status=status)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
