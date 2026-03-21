
import random

QUESTION_BANK = {
    "Backend Developer": [
        "What is the difference between REST and RESTful services?",
        "How do you handle authentication in a backend application?",
        "Explain the purpose of middleware.",
        "What is database normalization?",
        "How do you optimize API performance?",
        "What is the difference between SQL and NoSQL?",
        "How do you manage error handling in APIs?",
    ],
    "Frontend Developer": [
        "What is the difference between responsive and adaptive design?",
        "How do you manage state in a frontend application?",
        "Explain the virtual DOM.",
        "What is event bubbling?",
        "How do you improve web page performance?",
        "What are the benefits of component-based architecture?",
        "How do you handle browser compatibility issues?",
    ],
    "Full Stack Developer": [
        "How do frontend and backend communicate?",
        "What is the role of APIs in full stack development?",
        "How do you design a scalable web application?",
        "How do you manage authentication across the stack?",
        "Explain how you would debug an issue end-to-end.",
        "What is the difference between monolith and microservices?",
        "How do you structure a full stack project?",
    ],
    "Data Scientist": [
        "What is the difference between supervised and unsupervised learning?",
        "How do you handle missing data?",
        "What is overfitting?",
        "Explain feature engineering.",
        "How do you evaluate a machine learning model?",
        "What is the difference between classification and regression?",
        "How do you choose the right metric for a model?",
    ],
    "AI & ML Developer": [
        "What is the difference between AI, ML, and Deep Learning?",
        "How do you train and validate a model?",
        "What is the purpose of loss functions?",
        "Explain model overfitting and underfitting.",
        "How do you tune hyperparameters?",
        "What is the role of embeddings?",
        "How do you deploy a machine learning model?",
    ],
    "Tester": [
        "What is the difference between manual and automated testing?",
        "What is a test case?",
        "How do you write a good bug report?",
        "What is regression testing?",
        "What is smoke testing?",
        "How do you prioritize test scenarios?",
        "What is the role of QA in software development?",
    ],
    "Designer": [
        "What makes a design user-friendly?",
        "What is the difference between UX and UI?",
        "How do you approach a new design project?",
        "How do you use feedback to improve a design?",
        "What is the importance of consistency in design?",
        "How do you choose colors and typography?",
        "How do you design for accessibility?",
    ],
    "Python Developer": [
        "What are Python's key strengths?",
        "What is the difference between a list and a tuple?",
        "Explain what a module is in Python.",
        "What is list comprehension?",
        "What is the difference between deep copy and shallow copy?",
        "How do you handle exceptions in Python?",
        "What is object-oriented programming in Python?",
    ],
    "Java Developer": [
        "What is the difference between JDK, JRE, and JVM?",
        "What is object-oriented programming?",
        "What is the difference between an interface and an abstract class?",
        "Explain exception handling in Java.",
        "What is multithreading?",
        "What is the purpose of the garbage collector?",
        "What are collections in Java?",
    ],
    "UI Developer": [
        "What is the difference between UI and UX?",
        "How do you build a clean interface?",
        "What are the principles of visual hierarchy?",
        "How do you keep a design consistent?",
        "What is accessibility in UI development?",
        "How do you improve user interaction?",
        "What makes a dashboard easy to use?",
    ],
}

DEFAULT_QUESTIONS = [
    "Tell me about yourself.",
    "What are your strengths?",
    "What are your weaknesses?",
    "Why should we hire you?",
    "Where do you see yourself in five years?",
]


def generate_questions(role=None):

    import random

    # INTRO (ALWAYS FIRST)
    intro = [
        "Tell me about yourself."
    ]

    # DOMAIN QUESTIONS
    domain_q = QUESTION_BANK.get(role, [])
    random.shuffle(domain_q)

    # choose 10 domain questions (or max available)
    domain_count = min(10, len(domain_q))
    selected_domain = domain_q[:domain_count]

    # HR QUESTIONS
    hr = [
        "What are your strengths?",
        "What are your weaknesses?",
        "Why should we hire you?",
        "Where do you see yourself in 5 years?",
        "How do you handle pressure?",
        "What motivates you?",
        "Tell me about a challenge you faced.",
        "Why do you want this job?"
    ]

    random.shuffle(hr)

    # choose remaining to make total 15–20
    total_questions = random.randint(15, 20)
    hr_count = total_questions - 1 - domain_count   # -1 for intro

    selected_hr = hr[:hr_count]

    # FINAL FLOW (NO MIXING)
    final_questions = intro + selected_domain + selected_hr

    return final_questions