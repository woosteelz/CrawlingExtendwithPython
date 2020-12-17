from flask import Flask, render_template, request, redirect, send_file
from crawler import get_jobs
from exporter import save_to_file

app = Flask("SuperScrapper")

existJob = {}     ##Fake DB

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  word = request.args.get("word")
  if word:
    word = word.lower()
    fromDB = existJob.get(word)
    if fromDB:
      jobs = fromDB
    else:
      jobs = get_jobs(word)
      existJob[word] = jobs
  else:
    return redirect("/")
  return render_template("report.html", searchingBy = word, resultsNum = len(jobs), jobs = jobs)

@app.route("/export")
def export():
  try:
    word = request.args.get("word")
    if not word:
      raise Exception()
    word = word.lower()
    jobs = existJob.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file('jobs.csv', mimetype='application/x-csv', attachment_filename='report.csv', as_attachment=True)
  except:
    return redirect("/")

app.run(host = "0.0.0.0")