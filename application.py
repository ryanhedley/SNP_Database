from flask import Flask, render_template, request, redirect, url_for
import sqlite_queries as queries


app = Flask(__name__)


db_name = "snpdata.db"


@app.route("/")
def home():

    try:
        count = queries.count(db_name)
    except:
         count = 0

    return render_template("home.html", count=count)


@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/test")
def manifest():

    test = queries.test(db_name)

    return render_template("test.html", test=test)

@app.route("/bpm_upload")
def bpm_upload():

    queries.add_manifest(db_name)
    return redirect(url_for('upload'))

@app.route("/gtc_upload")
def gtc_upload():

    queries.add_multi_gtc_files(db_name)
    return redirect(url_for('upload'))




# @app.route('/', methods=['POST'])
# def upload_file():
#     gtc_files = request.files.getlist('gtc_files')
#     gtc_file_list = []
#     for file in gtc_files:
#         print(file.filename)
#         gtc_file_list.append(file.filename)


#     return render_template("success.html", gtc_file_names=gtc_file_list)


