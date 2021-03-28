from flask import Flask, render_template, request, redirect, url_for
import sqlite_queries as queries


app = Flask(__name__)



db_name = "snpdata.db"


@app.route("/")
def home():

    try:
        manifest_count = queries.count_manifest(db_name)
    except:
         manifest_count = 0

    try:
        patients_count = queries.count_patients(db_name)
    except:
         patients_count = 0

    return render_template("home.html", manifest_count=manifest_count, patients_count=patients_count)


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

    results, summary = queries.search_snp(db_name, snp_names)

    return render_template("results.html", results=results, summary=summary)


@app.route("/bpm_upload")
def bpm_upload():

    queries.add_manifest(db_name)
    return redirect(url_for('home'))
    

@app.route("/gtc_upload")
def gtc_upload():

    queries.add_multi_gtc_files(db_name)
    return redirect(url_for('home'))

@app.route("/all")
def all_snps():

    all_snps = queries.all_snp(db_name)

    return render_template("all.html", all_snps=all_snps)


@app.route("/hfe")
def hfe_snps():


    hfe_snps = queries.hfe_snps(db_name)

    return render_template("hfe.html", hfe_snps=hfe_snps)


