import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, render_template, request, redirect, session, jsonify
from ai_engine.question_generator import generate_questions
from ai_engine.answer_evaluator import evaluate_answer
from database.db import get_db_connection

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

app.secret_key = "ai_interview_secret_key"


# ================= HOME =================

@app.route("/")
def home():
    return render_template("index.html")


# ================= REGISTER =================

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method=="POST":

        name=request.form["name"]
        email=request.form["email"]

        conn=get_db_connection()
        cursor=conn.cursor()

        # check old user
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user=cursor.fetchone()

        if user:
            session["user_name"]=user["name"]
            session["email"]=user["email"]
        else:
            cursor.execute(
                "INSERT INTO users(name,email) VALUES(?,?)",
                (name,email)
            )
            conn.commit()

            session["user_name"]=name
            session["email"]=email

        cursor.close()
        conn.close()

        return redirect("/ready")

    return render_template("register.html")


# ================= READY =================

@app.route("/ready")
def ready():

    name=session.get("user_name","User")

    return render_template("ready.html",name=name)


# ================= INTERVIEW =================

@app.route("/interview")
def interview():

    questions=generate_questions()

    session["questions"]=questions
    session["question_index"]=0
    session["answers"]=[]
    session["scores"]=[]

    return render_template("interview.html")


# ================= GET QUESTION =================

@app.route("/get_question")
def get_question():

    questions=session.get("questions",[])
    index=session.get("question_index",0)

    if index>=len(questions):
        return jsonify({"finished":True})

    return jsonify({
        "question":questions[index],
        "finished":False
    })


# ================= SUBMIT ANSWER =================

@app.route("/submit_answer",methods=["POST"])
def submit_answer():

    data=request.get_json()
    answer=data.get("answer","")

    questions=session.get("questions",[])
    index=session.get("question_index",0)

    if index>=len(questions):
        return jsonify({"status":"finished"})

    question=questions[index]

    score=evaluate_answer(question,answer)

    answers=session.get("answers",[])
    scores=session.get("scores",[])

    answers.append(answer)
    scores.append(score)

    session["answers"]=answers
    session["scores"]=scores
    session["question_index"]=index+1

    return jsonify({"status":"ok"})


# ================= RESULT =================

@app.route("/result")
def result():

    scores=session.get("scores",[])

    if len(scores)==0:
        total_score=0
    else:
        total_score=round(sum(scores)/len(scores))

    name=session.get("user_name","User")
    email=session.get("email","")

    conn=get_db_connection()
    cursor=conn.cursor()

    cursor.execute(
        "INSERT INTO results(name,email,score) VALUES(?,?,?)",
        (name,email,total_score)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return render_template("result.html",score=total_score)


# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():

    conn=get_db_connection()
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM results ORDER BY id DESC")
    results=cursor.fetchall()

    scores=[row["score"] for row in results]
    dates=[f"Interview {i+1}" for i in range(len(scores))]

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        results=results,
        scores=scores,
        dates=dates
    )


# ================= LOGOUT =================

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__=="__main__":
    app.run(debug=True)