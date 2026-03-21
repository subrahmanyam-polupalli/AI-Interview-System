
import os
import sys
import json
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, render_template, request, redirect, session, jsonify, abort, url_for
from ai_engine.question_generator import generate_questions
from ai_engine.answer_evaluator import evaluate_answer, generate_feedback
from database.db import get_db_connection

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)

app.secret_key = os.getenv("SECRET_KEY", "ai_interview_secret_key_change_me")

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

DOMAIN_OPTIONS = [
    "Backend Developer",
    "Frontend Developer",
    "Full Stack Developer",
    "Data Scientist",
    "AI & ML Developer",
    "Tester",
    "Designer",
    "Python Developer",
    "Java Developer",
    "UI Developer",
]

def is_admin():
    return session.get("is_admin", False)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        age = request.form.get("age", "").strip()

        if not name or not email or not age:
            return render_template("register.html", error="Please fill all fields.")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user:
            user_id = user["id"]
            cursor.execute(
                "UPDATE users SET name = ?, age = ? WHERE id = ?",
                (name, age, user_id),
            )
        else:
            cursor.execute(
                "INSERT INTO users(name, email, age) VALUES(?, ?, ?)",
                (name, email, age),
            )
            user_id = cursor.lastrowid

        conn.commit()
        cursor.close()
        conn.close()

        session["user_id"] = user_id
        session["user_name"] = name
        session["email"] = email
        session["age"] = age
        session.pop("role", None)

        return redirect(url_for("domain_select"))

    return render_template("register.html")


@app.route("/domain", methods=["GET", "POST"])
def domain_select():
    if "user_id" not in session:
        return redirect(url_for("register"))

    if request.method == "POST":
        role = request.form.get("role", "").strip()
        if role not in DOMAIN_OPTIONS:
            return render_template("domain.html", domains=DOMAIN_OPTIONS, error="Please choose a valid role.")

        session["role"] = role
        return redirect(url_for("ready"))

    return render_template("domain.html", domains=DOMAIN_OPTIONS)


@app.route("/ready")
def ready():
    name = session.get("user_name", "User")
    role = session.get("role", "Your chosen role")
    return render_template("ready.html", name=name, role=role)


@app.route("/interview")
def interview():
    if "user_id" not in session or "role" not in session:
        return redirect(url_for("register"))

    questions = generate_questions(session["role"])
    session["questions"] = questions
    session["question_index"] = 0
    session["answers"] = []
    session["scores"] = []

    return render_template("interview.html", role=session["role"], name=session.get("user_name", "User"))


@app.route("/get_question")
def get_question():
    questions = session.get("questions", [])
    index = session.get("question_index", 0)

    if index >= len(questions):
        return jsonify({"finished": True})

    return jsonify({
        "question": questions[index],
        "finished": False
    })


@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    data = request.get_json(silent=True) or {}
    answer = (data.get("answer", "") or "").strip()

    questions = session.get("questions", [])
    index = session.get("question_index", 0)

    if index >= len(questions):
        return jsonify({"status": "finished"})

    question = questions[index]
    role = session.get("role", "")

    score = evaluate_answer(question, answer, role)

    answers = session.get("answers", [])
    scores = session.get("scores", [])

    answers.append(answer)
    scores.append(score)

    session["answers"] = answers
    session["scores"] = scores
    session["question_index"] = index + 1

    return jsonify({"status": "ok", "score": score})


@app.route("/result")
def result():
    if "user_id" not in session:
        return redirect(url_for("register"))

    scores = session.get("scores", [])
    answers = session.get("answers", [])
    questions = session.get("questions", [])
    role = session.get("role", "Unknown")

    if len(scores) == 0:
        total_score = 0
    else:
        total_score = round(sum(scores) / len(scores))

    feedback = generate_feedback(
        {
            "role": role,
            "questions": questions,
            "answers": answers,
            "scores": scores,
            "total_score": total_score,
        }
    )

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO results(user_id, name, email, role, score, answers_json, feedback, created_at)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session.get("user_id"),
            session.get("user_name", "User"),
            session.get("email", ""),
            role,
            total_score,
            json.dumps({"questions": questions, "answers": answers, "scores": scores}),
            feedback,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()

    return render_template("result.html", score=total_score, feedback=feedback, role=role)


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("register"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM results WHERE user_id = ? ORDER BY id DESC",
        (session["user_id"],),
    )
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    scores = [row["score"] for row in results]
    dates = [f"Interview {i+1}" for i in range(len(scores))]

    return render_template(
        "dashboard.html",
        results=results,
        scores=scores,
        dates=dates,
        view_mode="user",
        title=f"{session.get('user_name', 'User')}'s Dashboard",
        subtitle=f"Role: {session.get('role', 'N/A')}",
    )


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin_dashboard"))
        return render_template("admin_login.html", error="Invalid admin password.")

    return render_template("admin_login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    if not is_admin():
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM results ORDER BY id DESC")
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    scores = [row["score"] for row in results]
    dates = [f"Interview {i+1}" for i in range(len(scores))]

    return render_template(
        "dashboard.html",
        results=results,
        scores=scores,
        dates=dates,
        view_mode="admin",
        title="Admin Dashboard",
        subtitle="All interview results",
    )


@app.route("/retry")
def retry():
    session.pop("questions", None)
    session.pop("question_index", None)
    session.pop("answers", None)
    session.pop("scores", None)
    return redirect(url_for("interview"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
