from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

@app.route("/", methods=["GET", "POST"])
def index():
    forecast_by_day = None
    error = None
    city = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric",
                "lang": "it"
            }

            try:
                response = requests.get(FORECAST_URL, params=params)
                data = response.json()

                if data.get("cod") == "200":
                    daily_data = {}

                    for entry in data["list"]:
                        # Dividiamo la stringa "2026-02-16 12:00:00" in data e ora
                        dt_parts = entry["dt_txt"].split(" ")
                        date_str = dt_parts[0]
                        time_str = dt_parts[1]
                        
                        temp = entry["main"]["temp"]
                        
                        if date_str not in daily_data:
                            daily_data[date_str] = {
                                "temps": [],
                                "description": entry["weather"][0]["description"],
                                "icon": entry["weather"][0]["icon"]
                            }
                        
                        # Se l'orario è mezzogiorno, aggiorniamo icona e descrizione 
                        # per avere quella più rappresentativa del giorno (non quella notturna)
                        if "12:00:00" in time_str:
                            daily_data[date_str]["description"] = entry["weather"][0]["description"]
                            daily_data[date_str]["icon"] = entry["weather"][0]["icon"]

                        daily_data[date_str]["temps"].append(temp)

                    # Liste per la traduzione in italiano
                    giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
                    mesi = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
                            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

                    forecast_by_day = {}

                    for date_str, info in daily_data.items():
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                        
                        giorno_nome = giorni[date_obj.weekday()]
                        mese_nome = mesi[date_obj.month - 1]
                        formatted_date = f"{giorno_nome} {date_obj.day} {mese_nome}"

                        temps = info["temps"]

                        forecast_by_day[formatted_date] = {
                            "min": round(min(temps), 1),
                            "max": round(max(temps), 1),
                            "description": info["description"],
                            "icon": info["icon"]
                        }
                else:
                    error = data.get("message", "Città non trovata!").capitalize()
            
            except Exception as e:
                error = "Errore durante la connessione al servizio meteo."

    return render_template("index.html", forecast=forecast_by_day, error=error, city=city)

if __name__ == "__main__":
    app.run(debug=True)

