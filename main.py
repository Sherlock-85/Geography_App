import datetime
from flask import Flask, render_template, request, send_file
import pandas as pd
from geopy.geocoders import Nominatim


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/success', methods=['POST'])
def success():
    global filename
    if request.method == "POST":
        # 'file' is the name of the input in index.html
        file = request.files['file']
        try:
            df = pd.read_csv(file)
            gc = Nominatim(user_agent="app-name")
            df['coordinates'] = df["Address"].apply(gc.geocode)
            df['Latitude'] = df['coordinates'].apply(lambda x: x.latitude if x is not None else None)
            df['Longitude'] = df['coordinates'].apply(lambda x: x.longitude if x is not None else None)
            # drop the coordinates column
            df = df.drop("coordinates", 1)
            # handle multiple people uploading files
            filename = datetime.datetime.now().strftime("uploads/%Y-%m-%d-%H-%M-%S-%f"+".csv")
            df.to_csv(filename, index=None)
            return render_template("index.html", text=df.to_html(), btn='download.html')
        except:
            return render_template("index.html", text="Please make sure you have an address column in your csv file.")


@app.route('/download')
def download():
    return send_file(filename, attachment_filename='yourfile.csv', as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
