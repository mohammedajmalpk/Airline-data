from flask import Flask,request,render_template
from flaskext.mysql import MySQL 

mysql = MySQL()
app = Flask(__name__,template_folder='template')
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'airport'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def my_form():
	import pandas as pd
	import mysql.connector as con
	import numpy as np

	mydb=con.connect(host='localhost',port='3306',user='root',password='',database='airport')
	columns = ['Airline ID','Name','Alias','IATA','ICAO','Callsign','Country','Active']
	df = pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat",sep=',',index_col=False,
		       names=columns,header=0)
	df_1=df.astype(object).where(pd.notnull(df), None)
	data=df_1.iloc[:,:].values.tolist()
	mycursor=mydb.cursor()
	qry="insert into airport_data values(%s,%s,%s,%s,%s,%s,%s,%s)"
	truncate_qry = "TRUNCATE TABLE airport_data;"
	mycursor.execute(truncate_qry)
	mydb.commit()
	for row in data:
	    mycursor.execute(qry,tuple(row))
	mydb.commit()
	return render_template('airways.html')
@app.route('/',methods=['POST'])
def information():
    
    airline = request.form['Aid']
    cursor = mysql.connect().cursor()
    cursor.execute("select * from airport_data where Name = '" +airline+"'")
    #confirm = cursor.fetchall()
    data = cursor.fetchall()
    cursor.close()
    return render_template('airways.html', details = data)

if __name__ == "__main__": 
    app.run(debug=True)

