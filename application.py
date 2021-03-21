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


@app.route("/search")
def manifest():
    return render_template("search.html")


@app.route("/results", methods=["GET", "POST"])
def results():

    if request.method == "POST":
        snp_names = request.form.get("snp_name")
        snp_names = f"'{snp_names}'"
    else:
        snp_names = ""

    results = queries.search_snp(db_name, snp_names)

    return render_template("results.html", results=results)


@app.route("/bpm_upload")
def bpm_upload():

    queries.add_manifest(db_name)
    return redirect(url_for('upload'))
    

@app.route("/gtc_upload")
def gtc_upload():

    queries.add_multi_gtc_files(db_name)
    return redirect(url_for('upload'))



