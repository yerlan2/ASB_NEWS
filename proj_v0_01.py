import cx_Oracle
from flask import Flask, request, session, render_template, redirect, url_for, make_response, jsonify
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

def select_user_where(*user_credentials):
	users = []
	try:
		cur = conn.cursor()
		p_email, p_password = ':1', ':2'
		sql_select = f"SELECT * FROM TABLE ( users_pkg.select_user_where({p_email}, {p_password}) )"
		cur.execute(sql_select, user_credentials)
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
	categories = []
	try:
		cur = conn.cursor()
		sql_select = "SELECT * FROM TABLE ( categories_pkg.select_all_categories() )"
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
		sql_select = f"SELECT {select} FROM ARTICLES1, SOURCES1, CATEGORIES1 WHERE ARTICLES1.source_id=SOURCES1.id AND ARTICLES1.category_id=CATEGORIES1.id ORDER BY publishedAt DESC"	
		cur.execute(sql_select)
		articles = cur.fetchall()
	except Exception as err:
		print('Exception occured while fetching the records ', err)
	else:
		print('Query Completed.')
	finally:
		cur.close()
	return articles

def select_from_articles_where(select, where, *data):
	articles = []
	try:
		cur = conn.cursor()
		sql_select = f"SELECT {select} FROM ARTICLES1, SOURCES1, CATEGORIES1 WHERE ARTICLES1.source_id=SOURCES1.id AND ARTICLES1.category_id=CATEGORIES1.id AND {where} ORDER BY publishedAt DESC"
		cur.execute(sql_select, data)
		articles = cur.fetchall()
	except Exception as err:
		print('Exception occured while fetching the records ', err)
	else:
		print('Query Completed.')
	finally:
		cur.close()
	return articles

def insert_into_articles(*user_data):
	err = []
	source, category, author, title, description, url, urlToImage, content = user_data
	try:
		cur = conn.cursor()
		user_data = (source, category, author, title, description, url, urlToImage, content)
		cur.callproc('articles_pkg.insert_article', user_data)
	except cx_Oracle.IntegrityError as e:
		errorObj, = e.args
		err.append("ERROR: " + str(errorObj))
		print('ERROR while inserting the data ', errorObj)
	else:
		print('Insert Completed.')
	finally:
		cur.close()
	return err


def insert_into_users_articles(*user_data):
	err = []
	user_id, article_id = user_data
	try:
		cur = conn.cursor()
		user_data = (user_id, article_id)
		cur.callproc('users_articles_pkg.insert_users_articles', user_data)
	except cx_Oracle.IntegrityError as e:
		errorObj, = e.args
		print('ERROR while inserting the data ', errorObj)
		err.append("Star already exists.")
	else:
		print('Insert Completed.')
	finally:
		cur.close()
	return err

def delete_from_users_articles(*user_data):
	err = []
	user_id, article_id = user_data
	try:
		cur = conn.cursor()
		user_data = (user_id, article_id)
		cur.callproc('users_articles_pkg.delete_users_articles', user_data)
	except cx_Oracle.IntegrityError as e:
		errorObj, = e.args
		print('ERROR while inserting the data ', errorObj)
		err.append("Star already exists.")
	else:
		print('Insert Completed.')
	finally:
		cur.close()
	return err


def select_users_articles_where(*user_id_credentials):
	users_articles = []
	try:
		cur = conn.cursor()
		p_user_id = ':1'
		sql_select = f"SELECT * FROM TABLE ( users_articles_pkg.select_users_articles_where({p_user_id}) )"
		cur.execute(sql_select, user_id_credentials)
		users_articles = cur.fetchall()
	except Exception as err:
		print('Exception occured while fetching the records ', err)
	else:
		print('Query Completed.')
	finally:
		cur.close()
	return users_articles


@app.route('/')
@app.route('/home')
def index():
	err = []
	if 'email' in session and 'password' in session:
		email = session['email']
		password = session['password']
		users = select_user_where(email, password)
		if len(users) <= 0:
			err.append("Username OR password is incorrect.")
			return render_template('login.html', errors=err)
		users_articles = select_users_articles_where(users[0][0])
		articles_id_ls = []
		for x in users_articles:
			articles_id_ls.append(x[1])
		articles = select_from_articles('articles1.id, sources1.name, categories1.name, author, title, description, url, urlToImage, publishedAt, content')
		categories = select_from_categories()
		return render_template('home.html', session=session, users=users, articles=articles, categories=categories, articles_id_ls=articles_id_ls)
	else:
		return redirect('/login')


@app.route('/c/<string:name>')
def category_page(name):
	err = []
	if 'email' in session and 'password' in session:
		email = session['email']
		password = session['password']
		users = select_user_where(email, password)
		if len(users) <= 0:
			err.append("Username OR password is incorrect.")
			return render_template('login.html', errors=err)
		users_articles = select_users_articles_where(users[0][0])
		articles_id_ls = []
		for x in users_articles:
			articles_id_ls.append(x[1])
		categories = select_from_categories()
		articles = select_from_articles_where('articles1.id, sources1.name, categories1.name, author, title, description, url, urlToImage, publishedAt, content', 'categories1.name=:1', name)
		return render_template('home.html', session=session, users=users, categories=categories, articles=articles, articles_id_ls=articles_id_ls)
	else:
		return redirect('/login')


@app.route('/search', methods=['GET'])
def search():
	err = []
	if 'email' in session and 'password' in session:
		email = session['email']
		password = session['password']
		if request.method == 'GET':
			q = request.args['q'].lower()
			users = select_user_where(email, password)
			if len(users) <= 0:
				err.append("Username OR password is incorrect.")
				return render_template('login.html', errors=err)
			users_articles = select_users_articles_where(users[0][0])
			articles_id_ls = []
			for x in users_articles:
				articles_id_ls.append(x[1])
			articles = select_from_articles_where(
				'articles1.id, sources1.name, categories1.name, author, title, description, url, urlToImage, publishedAt, content', 
				f"(LOWER(title) LIKE '%{q}%' OR LOWER(description) LIKE '%{q}%' OR LOWER(categories1.name) LIKE '%{q}%' OR LOWER(sources1.name) LIKE '%{q}%' OR LOWER(author) LIKE '%{q}%' OR LOWER(content) LIKE '%{q}%' )"
			)
			categories = select_from_categories()
			return render_template('home.html', session=session, users=users, articles=articles, categories=categories, articles_id_ls=articles_id_ls)
	else:
		return redirect('/login')


@app.route('/register', methods=['POST', 'GET'])
def register():
	err = []
	categories = select_from_categories()
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		err = insert_into_users(
			email, password, first_name, last_name
		)
		if len(err) <= 0:
			return redirect(url_for('login'))
		else:
			return render_template('register.html', categories=categories, errors=err)
	else:
		return render_template('register.html', categories=categories)


@app.route('/login', methods=['POST', 'GET'])
def login():
	err = []
	if request.method == 'POST':
		email = request.form['email']
		password = sha256(request.form['password'].encode("UTF-8")).hexdigest()
		users = select_user_where(email, password)
		categories = select_from_categories()
		if len(users) > 0:
			session['email'] = email
			session['password'] = password
			if session['email']=='admin@email.com' \
			and session['password']==sha256('admin'.encode("UTF-8")).hexdigest():
				return redirect("/admin")
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


@app.route('/admin', methods=['POST', 'GET'])
def admin():
	err = []
	categories = select_from_categories()
	if request.method == 'POST':
		source = request.form['source']
		category = request.form['category']
		author = request.form['author']
		title = request.form['title']
		description = request.form['description']
		url = request.form['url']
		urlToImage = request.form['urlToImage']
		content = request.form['content']
		err = insert_into_articles(source, category, author, title, description, url, urlToImage, content)
		if len(err) <= 0:
			return redirect(url_for('index'))
		else:
			return render_template('admin.html', categories=categories, errors=err)
	else:
		if 'email' in session \
		and 'password' in session \
		and session['email']=='admin@email.com' \
		and session['password']==sha256('admin'.encode("UTF-8")).hexdigest():
			categories = select_from_categories()
			return render_template('admin.html', session=session, categories=categories)
		else:
			return redirect('/logout')


@app.route('/addstar', methods=['POST', 'GET'])
def addstar():
	if request.method == 'POST':
		req = request.get_json()
		err = insert_into_users_articles(
			req['user_id'], req['article_id']
		)
		if len(err) <= 0:
			res = make_response(jsonify({'message':"ok"}), 200)
			return res;
		else:
			res = make_response(jsonify({'message':"not ok"}), 400)
			return res;
	else:
		res = make_response(jsonify({'message':"not Post"}), 400)
		return res;


@app.route('/removestar', methods=['POST', 'GET'])
def removestar():
	if request.method == 'POST':
		req = request.get_json()
		print(req)
		err = delete_from_users_articles(
			req['user_id'], req['article_id']
		)
		if len(err) <= 0:
			res = make_response(jsonify({'message':"ok"}), 200)
			return res;
		else:
			res = make_response(jsonify({'message':"not ok"}), 400)
			return res;
	else:
		res = make_response(jsonify({'message':"not Post"}), 400)
		return res;


@app.route('/favorite')
def favorite():
	err = []
	articles = []
	if 'email' in session and 'password' in session:
		email = session['email']
		password = session['password']
		users = select_user_where(email, password)
		if len(users) <= 0:
			err.append("Username OR password is incorrect.")
			return render_template('login.html', errors=err)
		users_articles = select_users_articles_where(users[0][0])
		if len(users_articles) > 0:
			articles_num = ':1'
			for i in range(2, len(users_articles)+1):
				articles_num += ', :'+ str(i)
			articles_id_ls = []
			for x in users_articles:
				articles_id_ls.append(x[1])
			articles = select_from_articles_where('articles1.id, sources1.name, categories1.name, author, title, description, url, urlToImage, publishedAt, content', f'articles1.id IN ({articles_num})', *articles_id_ls)
			categories = select_from_categories()
			return render_template('home.html', session=session, users=users, articles=articles, categories=categories, articles_id_ls=articles_id_ls)
		else:
			categories = select_from_categories()
			return render_template('home.html', session=session, users=users, articles=articles, categories=categories)
	else:
		return redirect('/login')


@app.route('/predict', methods=['POST'])
def predict_category():
	if request.method == 'POST':
		req = request.get_json()
		from ml import predict
		category = predict(req['content'])
		res = make_response(jsonify({'category': category[0]}), 200)
		return res
	else:
		res = make_response(jsonify({'message':"not Post"}), 400)
		return res;


import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity


def get_recommendations(cosine_sim, titles, article_ids):
	id = article_ids
	sim_scores = []
	for idx in id:
		sim_scores = sim_scores + list(enumerate(cosine_sim[idx]))
		sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
		project_indices = [i[0] for i in sim_scores]
	return titles.iloc[project_indices][len(id):]


@app.route('/recommendation')
def recommendation():
	err = []
	articles = []
	if 'email' in session and 'password' in session:
		email = session['email']
		password = session['password']
		users = select_user_where(email, password)
		if len(users) <= 0:
			err.append("Username OR password is incorrect.")
			return render_template('login.html', errors=err)
		categories = select_from_categories()
		users_articles = select_users_articles_where(users[0][0])
		if len(users_articles) > 0:
			articles_id_ls = []
			for x in users_articles:
				articles_id_ls.append(x[1])
			articles = select_from_articles('articles1.id, sources1.name, categories1.name, author, title, description, url, urlToImage, publishedAt, content')
			df = pd.DataFrame(np.array(articles), columns=['id', 'source', 'category', 'author', 'title', 'description', 'url', 'urlToImage', 'publishedAt', 'content'])
			df = df.set_index('id')
			df['text'] = df['category'] + " " + df['title'] + " " + df['description']
			tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
			tfidf_matrix = tf.fit_transform(df['text'])
			cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
			titles = df['title']
			indices = pd.Series(df.index, index=df['title'])
			recommended = get_recommendations(cosine_sim, titles, articles_id_ls).head(25)
			recommended = recommended.index.values.tolist()
			if len(recommended) > 0:
				articles_num = ':1'
				for i in range(2, len(recommended)+1):
					articles_num += ', :'+ str(i)
				print(recommended)
				articles = select_from_articles_where('articles1.id, sources1.name, categories1.name, author, title, description, url, urlToImage, publishedAt, content', f'articles1.id IN ({articles_num})', *recommended)
				return render_template('home.html', session=session, users=users, articles=articles, categories=categories, articles_id_ls=articles_id_ls)
			else:
				return render_template('home.html', session=session, users=users, articles=articles, categories=categories)
		else:
			return render_template('home.html', session=session, users=users, articles=articles, categories=categories)
	else:
		return redirect('/login')


if __name__=="__main__":
	app.run(debug=True)


conn.close()

