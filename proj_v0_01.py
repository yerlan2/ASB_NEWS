import cx_Oracle
from flask import Flask, request, session, render_template, redirect, url_for
from hashlib import sha256

try:
    conn = cx_Oracle.connect('ora_proj2/hr@//localhost:1521/XE')
except Exception as err:
    print('Error while creating the connection ', err)


app = Flask(__name__)
app.secret_key = "secret_key"


def select_from_users():
	users = []
	try:
		cur = conn.cursor()
		sql_select = "SELECT * FROM TABLE ( users_pkg.select_all_users() )"
		cur.execute(sql_select)
		users = cur.fetchall()
	except Exception as err:
		print('Exception occured while fetching the records ', err)
	else:
		print('Query Completed.')
	finally:
		cur.close()
	return users

def select_from_users_where(select, where, *args):
	try:
		cur = conn.cursor()
		sql_select = f"SELECT {select} FROM USERS WHERE {where}"
		data = tuple(args)
		cur.execute(sql_select, data)
		users = cur.fetchall()
	except Exception as err:
		print('Exception occured while fetching the records ', err)
	else:
		print('Query Completed.')
	finally:
		cur.close()
	return users

def insert_into_users(*user_data):
	err = []
	email, password, first_name, last_name = user_data
	try:
		cur = conn.cursor()
		password = sha256(password.encode("UTF-8")).hexdigest()
		user_data = (email, password, first_name, last_name)
		cur.callproc('users_pkg.insert_user', user_data)
	except cx_Oracle.IntegrityError as e:
		errorObj, = e.args
		print('ERROR while inserting the data ', errorObj)
		err.append("Username already exists.")
	else:
		print('Insert Completed.')
	finally:
		cur.close()
	return err

def select_from_categories():
	try:
		cur = conn.cursor()
		sql_select = "SELECT * FROM CATEGORIES"	
		cur.execute(sql_select)
		categories = cur.fetchall()
	except Exception as err:
		print('Exception occured while fetching the records ', err)
	else:
		print('Query Completed.')
	finally:
		cur.close()
	return categories

def select_from_articles(select):
	articles = []
	try:
		cur = conn.cursor()
		sql_select = f"SELECT {select} FROM ARTICLES, SOURCES, CATEGORIES WHERE ARTICLES.source_id=SOURCES.id AND ARTICLES.category_id=CATEGORIES.id"	
		cur.execute(sql_select)
		articles = cur.fetchall()
	except Exception as err:
		print('Exception occured while fetching the records ', err)
	else:
		print('Query Completed.')
	finally:
		cur.close()
	return articles

def select_from_articles_where(select, where, *args):
	articles = []
	try:
		cur = conn.cursor()
		sql_select = f"SELECT {select} FROM ARTICLES, SOURCES, CATEGORIES WHERE ARTICLES.source_id=SOURCES.id AND ARTICLES.category_id=CATEGORIES.id AND {where}"
		data = args
		cur.execute(sql_select, data)
		articles = cur.fetchall()
	except Exception as err:
		print('Exception occured while fetching the records ', err)
	else:
		print('Query Completed.')
	finally:
		cur.close()
	return articles


@app.route('/')
@app.route('/home')
def index():
	err = []
	if 'email' in session and 'password' in session:
		email = session['email']
		password = session['password']
		users = select_from_users_where(
			"id, email, first_name, last_name", 
			"email=:1 AND password=:2", 
			email, password
		)
		if len(users) <= 0:
			err.append("Username OR password is incorrect.")
			return render_template('login.html', errors=err)
		articles = select_from_articles('articles.id, sources.name, categories.name, author, title, description, url, urlToImage, publishedAt, content')
		categories = select_from_categories()
		return render_template('home.html', users=users, articles=articles, categories=categories)
	else:
		return redirect('/login')


@app.route('/c/<string:name>')
def category_page(name):
	err = []
	if 'email' in session and 'password' in session:
		email = session['email']
		password = session['password']
		users = select_from_users_where(
			"id, email, first_name, last_name", 
			"email=:1 AND password=:2", 
			email, password
		)
		if len(users) <= 0:
			err.append("Username OR password is incorrect.")
			return render_template('login.html', errors=err)
		articles = select_from_articles_where('articles.id, sources.name, categories.name, author, title, description, url, urlToImage, publishedAt, content', 'categories.name=:1', name)
		categories = select_from_categories()
		return render_template('home.html', users=users, articles=articles, categories=categories)
	else:
		return redirect('/login')


@app.route('/search', methods=['GET'])
def search():
	err = []
	if 'email' in session and 'password' in session:
		if request.method == 'GET':
			q = request.args['q'].lower()
			users = select_from_users()
			articles = select_from_articles_where(
				'articles.id, sources.name, categories.name, author, title, description, url, urlToImage, publishedAt, content', 
				f"(LOWER(title) LIKE '%{q}%' OR LOWER(description) LIKE '%{q}%' OR LOWER(categories.name) LIKE '%{q}%' OR LOWER(sources.name) LIKE '%{q}%' OR LOWER(author) LIKE '%{q}%' OR LOWER(content) LIKE '%{q}%' )"
			)
			categories = select_from_categories()
			return render_template('home.html', users=users, articles=articles, categories=categories)
	else:
		return redirect('/login')


@app.route('/register', methods=['POST', 'GET'])
def register():
	err = []
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		err = insert_into_users(
			email, password, first_name, last_name
		)
		if len(err) <= 0:
			return redirect(url_for('register'))
		else:
			users = select_from_users()
			return render_template('register.html', users=users, errors=err)
	else:
		users = select_from_users()
		categories = select_from_categories()
		return render_template('register.html', users=users, categories=categories)


@app.route('/login', methods=['POST', 'GET'])
def login():
	err = []
	if request.method == 'POST':
		email = request.form['email']
		password = sha256(request.form['password'].encode("UTF-8")).hexdigest()
		users = select_from_users_where(
			"id, email, first_name, last_name", 
			"email=:1 AND password=:2", 
			email, password
		)
		categories = select_from_categories()
		if len(users) > 0:
			session['email'] = email
			session['password'] = password
			return redirect("/")
		else:
			err.append("Username OR password is incorrect.")
			return render_template('login.html', categories=categories, errors=err)
		# return redirect('/login')
	else:
		categories = select_from_categories()
		return render_template('login.html', categories=categories)


@app.route('/logout')
def logout():
	if 'email' in session and 'password' in session:
	del session['email']
	del session['password']
	return redirect('/login')


if __name__=="__main__":
	app.run(debug=True)


conn.close()

