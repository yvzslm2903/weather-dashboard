from flask import Flask, render_template, request
from datetime import datetime, timedelta
from models import WeatherRecord, Session

app = Flask(__name__)

@app.route("/")
def dashboard():
    days = request.args.get("days", default=2, type=int)
    grenze = datetime.now() + timedelta(days=days)

    session = Session()
    records = (session.query(WeatherRecord)
               .filter(WeatherRecord.time <= grenze)
               .order_by(WeatherRecord.time)
               .all())
    session.close()

    labels = [r.time.strftime("%d.%m. %H:%M") for r in records]
    temperaturen = [r.temperature for r in records]

    aktuell = None
    for r in records:
        if r.time >= datetime.now():
            aktuell = r
            break

    return render_template("dashboard.html",
                           labels=labels,
                           temperaturen=temperaturen,
                           anzahl=len(records),
                           days=days)

if __name__ == "__main__":
    app.run(debug=True)