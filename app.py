from flask import Flask, render_template, request, jsonify
from werkzeug.datastructures import FileStorage
import pandas as pd
from pkg.ocr_demo import ocr_main
import time 


app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")



@app.route('/project')
def project():  # put application's code here
    return render_template("project.html")


@app.route('/about')
def about():  # put application's code here
    return render_template("about.html")



@app.route("/upload", methods=("POST",))
def upload():
    file: FileStorage = request.files.get("file")
    save_path = "upload/pdf/demo.pdf"
    img_path = "upload/img/demo.png"
    file.save(save_path)
    # pdf2png(save_path, img_path)

    data = ocr_main.handler_pdf(save_path, img_path)

    file_name = f"static/{time.time().__str__()}.csv"
    # generate csv
    df = pd.DataFrame(data)
    df.to_csv(file_name)

    return jsonify({"code": 1, "data": data, "down": file_name})


if __name__ == '__main__':
    app.run(debug=True)
