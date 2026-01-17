from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import os
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv("EMAIL_USER"),
    MAIL_PASSWORD=os.getenv("EMAIL_PASS")
)


mail = Mail(app)

def run_topsis(file_path, weights, impacts, output_path):
    data = pd.read_csv(file_path)
    criteria = data.iloc[:, 3:].astype(float).values

    weights = np.array(weights, dtype=float)
    norm = criteria / np.sqrt((criteria ** 2).sum(axis=0))
    weighted = norm * weights

    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted[:, i].max())
            ideal_worst.append(weighted[:, i].min())
        else:
            ideal_best.append(weighted[:, i].min())
            ideal_worst.append(weighted[:, i].max())

    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = dist_worst / (dist_best + dist_worst)
    data['Topsis Score'] = score
    data['Rank'] = data['Topsis Score'].rank(ascending=False)

    data.to_csv(output_path, index=False)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        weights = request.form["weights"].split(",")
        impacts = request.form["impacts"].split(",")
        email = request.form["email"]

        if len(weights) != len(impacts):
            return "Weights and Impacts count mismatch"

        if not all(i in ['+','-'] for i in impacts):
            return "Impacts must be + or -"

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        output_path = os.path.join(RESULT_FOLDER, "result.csv")
        run_topsis(file_path, weights, impacts, output_path)

        msg = Message(
            subject="TOPSIS Result",
            sender=app.config['MAIL_USERNAME'],
            recipients=[email]
        )
        msg.body = "Please find attached TOPSIS result file."
        msg.attach("result.csv", "text/csv", open(output_path).read())
        mail.send(msg)

        return "Result sent to email successfully!"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
