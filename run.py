from flask import Flask, render_template, request, redirect, url_for, json, session, flash
from flask.ext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

mysql= MySQL()

app=Flask(__name__)
app.secret_key = 'super secret key'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='root'
app.config['MYSQL_DATABASE_DB']='demo'
app.config['MYSQL_DATABASE_HOST']='localhost'
mysql.init_app(app)

@app.route('/')
def home():
	return render_template('home.html', title='SignUp')
	
@app.route('/signUp', methods=['POST'])
def signUp():
	try:
		user_name=request.form['username']
		_password=request.form['password']
		if user_name and _password:
			print (user_name)
			connection=mysql.get_db()
			cursor = connection.cursor()
			hashed_password=generate_password_hash(_password)
			cursor.execute("""insert into user (user_name,password,hash_password) values (%s,%s,%s)""",(user_name,_password,hashed_password))
			connection.commit()
			flash("You are successfully registered!! Kindly login to continue")
			return redirect(url_for('loginPage'))
	except Exception as e:
		return json.dumps({'error':str(e)})
		
@app.route('/loginPage')
def loginPage():
	return render_template('home.html', title='Login')
		

	
@app.route('/login', methods=['POST'])
def login():
	try:
		user_name=request.form['login-username']
		_password=request.form['login-password']
		if user_name and _password:
			print (user_name)
			print (_password)
			connection=mysql.get_db()
			cursor = connection.cursor()
			hashed_password=generate_password_hash(_password)
			check_password=check_password_hash(hashed_password,_password)
			print (check_password)
			if check_password==True:
				cursor.execute("""select * from user where user_name=%s and password=%s""",(user_name,_password))
				data=cursor.fetchall()
				print (data)
				if len(data) is 1:
					flash("You are successfully logged in")
					session['username']=user_name
					return redirect(url_for('search'))
				else:
					return redirect(url_for('unauth_user'))
	except Exception as e:
		return json.dumps({'error':str(e)})
		
@app.route('/search')
def search():
	return render_template('search.html')
	
@app.route('/display', methods=['POST'])
def display():
	try:
		video_name=request.form['search_query']
		if video_name:
			print(video_name)
			connection=mysql.get_db()
			cursor = connection.cursor()
			cursor.execute("""select video_name from video where video_name like %s""",(video_name))
			data=cursor.fetchall()
			print (data)
			return render_template('display.html', data=data)
	except Exception as e:
		return json.dumps({'error':str(e)})
		
@app.route('/video', methods=['POST'])
def video():
	try:
		video_name='adele hello'
		if video_name:
			print(video_name)
			connection=mysql.get_db()
			cursor = connection.cursor()
			cursor.execute("""select video_url from video where video_name like %s""",(video_name))
			cursor.execute("""select video_id from video where video_name like %s""",(video_name))
			data=cursor.fetchall()
			cursor.execute("""select likes from like_dislike where video_id %s""",(data))
			data1=cursor.fetchall()
			cursor.execute("""select dislikes from like_dislike where video_id %s""",(data))
			data2=cursor.fetchall()
			cursor.execute("""select comments from comments where video_id %s""",(data))
			data3=cursor.fetchall()
			return render_template('video.html', data=video_name,data1=data1, data2=data2,data3=data3)
	except Exception as e:
		return json.dumps({'error':str(e)})
		
@app.route('/like', methods=['POST'])
def like():
	try:
		video_name='adele hello'
		if video_name:
			print(video_name)
			connection=mysql.get_db()
			cursor = connection.cursor()
			cursor.execute("""select video_id from video where video_name like %s""",(video_name))
			data=cursor.fetchall()
			cursor.execute("""update like_dislike set likes=likes+1 where video_id=%s""",(data))
			cursor.execute("""select likes from like_dislike where video_id=%s""",(data))
			data1=cursor.fetchall()
			return render_template('video.html',data1=data1)
	except Exception as e:
		return json.dumps({'error':str(e)})
		
@app.route('/disike', methods=['POST'])
def dislike():
	try:
		video_name='adele hello'
		if video_name:
			print(video_name)
			connection=mysql.get_db()
			cursor = connection.cursor()
			cursor.execute("""select video_id from video where video_name like %s""",(video_name))
			data=cursor.fetchall()
			cursor.execute("""update like_dislike set dislikes=dislikes+1 where video_id=%s""",(data))
			cursor.execute("""select dislikes from like_dislike where video_id=%s""",(data))
			data2=cursor.fetchall()
			return render_template('video.html',data2=data2)
	except Exception as e:
		return json.dumps({'error':str(e)})
		
# @app.route('/store_comment' methods=['POST'])
# def store_comment():
	# try:
		# video_name='adele hello'
		# comment=request.form('comment')
		# if comment:
			# print(comment)
			# connection=mysql.get_db()
			# cursor = connection.cursor()
			# cursor.execute("""insert into comments values)
			# data=cursor.fetchall()
			# cursor.execute("""update like_dislike set dislikes=dislikes+1 where video_id=%s""",(data))
			# cursor.execute("""select dislikes from like_dislike where video_id=%s""",(data))
			# data2=cursor.fetchall()
			# return render_template('video.html',data2=data2)
	# except Exception as e:
		# return json.dumps({'error':str(e)})
	
app.route('/logout')
def logout():
	session.pop('username',None)
	return render_template('home.html',title='Login')
	
@app.route('/unauth_user')
def unauth_user():
	return render_template('error_user.html')

if __name__=='__main__':
	app.run(debug=True)
	
