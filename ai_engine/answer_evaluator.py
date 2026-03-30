def evaluate_answer(question,answer):

    keypoints={
        "python":[
            "easy",
            "readable",
            "interpreted",
            "object oriented",
            "high level"
        ],

        "oops":[
            "encapsulation",
            "inheritance",
            "polymorphism",
            "abstraction"
        ],

        "machine learning":[
            "data",
            "training",
            "model",
            "prediction"
        ]
    }

    answer=answer.lower()

    score=0

    feedback=[]

    for topic in keypoints:

        if topic in question.lower():

            points=keypoints[topic]

            for p in points:

                if p in answer:

                    score+=2

                else:

                    feedback.append(p)

    score=min(score,10)

    return score