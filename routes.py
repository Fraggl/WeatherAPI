from flask import Flask, url_for, render_template, jsonify, request, g;
from app import app;
from flaskext.mysql import MySQL;
import datetime
import MySQLdb as mdb

@app.before_request
def db_connect():
    g.db = mdb.connect('localhost','root','ostfalia','WeatherDB')
    print "successfully connected"

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
    print "sucessfully disconnected"

@app.route('/')
def index():
    # index
    return "Hello Flask!"

@app.route('/api/')
def value():
    print "Commands"
    return "Commands: Now, 3h, 24h, date (/<year>/<month>/<day>), msg"

@app.route('/api/now')
def tempnow():
    cur = g.db.cursor()
    cur.execute("SELECT * FROM `TB_Weather` ORDER BY Ts DESC LIMIT 1")
    erg=cur.fetchall()
    return jsonify(results=erg)

@app.route('/api/3h')
def tempthreeh():
    cur = g.db.cursor()
    cur.execute("SELECT * FROM  `TB_Weather` ORDER BY Ts DESC LIMIT 18")
    erg=cur.fetchall()
    print erg
    return jsonify(results=erg)

@app.route('/api/3h/<string:command>')
def temptforvar(command):
    cmd = command
    if cmd == "high":
        query = ("SELECT * FROM TB_Weather WHERE Messwert = (SELECT MAX(Messwert) FROM `TB_Weather` ORDER BY Ts DESC LIMIT 18)")
        print "high"
    elif cmd == "low":
        query = ("SELECT * FROM TB_Weather WHERE Messwert = (SELECT MIN(Messwert) FROM `TB_Weather` ORDER BY Ts DESC LIMIT 18)")
        print "low"
    elif cmd == "avg":
        query = ("SELECT AVG(Messwert) FROM `TB_Weather` ORDER BY Ts DESC LIMIT 18")
        print "average"
    elif cmd == "avghour":
        query =("SELECT Ts, AVG( Messwert )FROM `TB_Weather` WHERE Ts >= DATE_SUB( CURRENT_TIMESTAMP( ), INTERVAL 1 DAY )GROUP BY HOUR( Ts )ORDER BY `TB_Weather`.`Ts` DESC LIMIT 3")
    else:
        print "nothing selected"
        return "possible commands for this route: /high /low /avg /avghour"
    cur = g.db.cursor()
cur.execute(query)
    erg=cur.fetchall()
    print "Route erfolgreich durchlaufen"
    return jsonify(results=erg)

@app.route('/api/24h')
def tempyesterday():
    cur = g.db.cursor()
    cur.execute("SELECT * FROM `TB_Weather` ORDER BY Ts DESC LIMIT 144")
    erg=cur.fetchall()
    print "Ausgabe Temperaturen der letzten 24h"
    return jsonify(results=erg)

@app.route('/api/24h/<string:command>')
def tempthreehvar(command):
    cmd = command
    if cmd == "high":
        query = ("SELECT * FROM TB_Weather WHERE Messwert = (SELECT MAX(Messwert) FROM `TB_Weather` ORDER BY Ts DESC LIMIT 144)")
        print "high"
    elif cmd == "low":
        query = ("SELECT * FROM TB_Weather WHERE Messwert = (SELECT MIN(Messwert) FROM `TB_Weather` ORDER BY Ts DESC LIMIT 144)")
        print "low"
    elif cmd == "avg":
        query = ("SELECT AVG(Messwert) FROM `TB_Weather` ORDER BY Ts DESC LIMIT 144")
        print "avg"
    elif cmd ==  "avghour":
        query = ("SELECT Ts, AVG( Messwert )FROM `TB_Weather` WHERE Ts >= DATE_SUB( CURRENT_TIMESTAMP( ), INTERVAL 1 DAY )GROUP BY HOUR( Ts )ORDER BY `TB_Weather`.`Ts` DESC LIMIT 24")
        print "avghour"
    else:
        print "nothing selected"
        return "possible commands for this route: /high /low /avg /avgall"
    cur = g.db.cursor()
    cur.execute(query)
    erg=cur.fetchall()
    print "Route erfolgreich durchlaufenn"
    return jsonify(results=erg)

@app.route('/api/date/<int:year>/<int:month>/<int:day>')
def tempdate(year, month, day):
    quest_date = datetime.date(year, month, day)
    print quest_date
    cur = g.db.cursor()
    query = ("SELECT * FROM TB_Weather WHERE DATE(Ts) = %s Limit 144")
    cur.execute(query, (quest_date))
    erg=cur.fetchall()
    return jsonify(results=erg)

@app.route('/api/date/<int:year>/<int:month>/<int:day>/<string:command>')
def tempthreehvartest(year, month, day, command):
    quest_date = datetime.date(year, month, day)
    print quest_date
    cmd = command
    if cmd == "high":
        query = ("SELECT * FROM (SELECT * FROM TB_Weather WHERE Messwert = (SELECT MAX(Messwert) FROM `TB_Weather` WHERE DATE(Ts) = %s ORDER BY Ts) ) AS MAXI WHERE DATE (Ts) =  %s")
        print "high"
    elif cmd == "low":
        query = ("SELECT * FROM (SELECT * FROM TB_Weather WHERE Messwert = (SELECT MIN(Messwert) FROM `TB_Weather` WHERE DATE(Ts) = %s ORDER BY Ts) ) AS MINI WHERE DATE (Ts) =  %s")
        print "low"
    elif cmd == "avg":
	 query = ("SELECT AVG( Messwert ) FROM (SELECT * FROM `TB_Weather` WHERE DATE(Ts) = %s ORDER BY Ts) AS AVG")
        print "average"
    elif cmd ==  "avghour":
        query = ("SELECT Ts, AVG( Messwert )FROM `TB_Weather` WHERE DATE(Ts) = %s GROUP BY HOUR( Ts )ORDER BY `TB_Weather`.`Ts` DESC")
    else:
        print "nothing selected"
        return "possible commands for this route: /high /low /avg /avghour"
    cur = g.db.cursor()
    if (cmd == "high") or (cmd == "low"):
        cur.execute(query, (quest_date, quest_date))
        erg=cur.fetchall()
    else:
        cur.execute(query, (quest_date))
        erg=cur.fetchall()
    print "Route erfolgreich durchlaufen"
    return jsonify(results=erg)


@app.route('/api/msg')
def msg():
    print Meldungen
    return "Meldungen - hier werden Meldungen ausgegeben"

@app.errorhandler(404)
def page_not_found(error):
    return "page not found"
    render_template('page_not_found.html'), 404

