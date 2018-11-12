
from flask import render_template, flash, redirect, url_for,session, request
from app import app
from app.twitter import Twitter
from app.forms import LoginForm, QueryForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/query', methods=['GET', 'POST'])
def query():
    form = QueryForm()
    if form.validate_on_submit():
        campaign_number = form.campaign_number.data
        table_name = form.table_name.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        url = 'http://localhost:5000/datatable?campaign_number=%s&table_name=%s&start_time=%s&end_time=%s' % (campaign_number, table_name, start_time, end_time)
        return redirect(url)
        #flash()
    return render_template('query.html', title='Input Query', form=form)

@app.route('/datatable', methods=['GET', 'POST'])
def datatable():
    account_number = 'gq1iff'
    campaign_number = request.args.get('campaign_number')
    table_name = request.args.get('table_name')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    values_dict = Twitter.get_data_from_user(account_number, campaign_number, 'ENGAGEMENT', table_name)
    return render_template('datatable.html', title='Data Table', data = values_dict)

@app.route('/twitter', methods=['GET', 'POST'])
def twitter():
    oauth_token, oauth_token_secret= Twitter.get_request_token()
    url = 'https://api.twitter.com/oauth/authorize?oauth_token=%s' % (oauth_token)
    return redirect(url)

@app.route('/callback', methods=['GET', 'POST'])
def callback():
    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    print("callback token:\n" + oauth_token + "\n")
    print("callback verifier:\n" + oauth_verifier + "\n")
    access_token, oauth_token_secret, user_id, screen_name = Twitter.get_access_token(oauth_token, oauth_verifier)
    user = {'username': screen_name}
    posts = []
    Twitter.create_sandbox_account(access_token, oauth)
    return render_template('index.html', title='Home', user=user, posts=posts)

