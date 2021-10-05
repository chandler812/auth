import os
import json
from flask import Flask, jsonify, g, render_template, request, redirect, session, url_for
from requests_oauthlib import OAuth2Session

app = Flask(__name__)

# Get this information by registering your app at https://developer.id.me
client_id              = '28bf5c72de76f94a5fb1d9454e347d4e'
client_secret          = '3e9f2e9716dba6ec74a2e42e90974828'
redirect_uri           = 'http://localhost:5000/callback'
authorization_base_url = 'https://api.id.me/oauth/authorize'
token_url              = 'https://api.id.me/oauth/token'
attributes_url         = 'https://api.id.me/api/public/v2/attributes.json'



@app.route("/")
def demo():
    return render_template('index.html')

@app.route("/callback")
def callback():
    # Exchange your code for an access token
    idme  = OAuth2Session(client_id, redirect_uri=redirect_uri)
    token = idme.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
    print("Token:")
    print(token)

    # At this point you can fetch a user's attributes but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token

    return redirect(url_for('.profile'))

@app.route("/profile")
def profile():
    # Fetching the user's attributes using an OAuth 2 token.
    idme = OAuth2Session(client_id, token=session['oauth_token'])
    #print(idme)
    user = idme.get(attributes_url)
    #g.user = user
    payload = user.json()
    #print("Payload:")
    #print(payload["email"])
    #print(user)
    #print(g.user)
    #g.user = payload
    #print(g.user)
    email = payload["email"]
    fname = payload["fname"]
    lname = payload["lname"]
    verified = payload["verified"]
    thisToken = session['oauth_token']
    accessToken = thisToken['access_token']

    session['profile'] = 'true'
    html_ret = "Hello, "+str(fname)+" "+str(lname)+"! You're verification status is: "+str(verified)+". We will contact you at "+str(email)+" with more information! Ohh and incase you need it... here is your OAuth Access Token: "+str(accessToken)
    #return jsonify(payload)
    return html_ret


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['DEBUG'] = "1"
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app.secret_key = os.urandom(24)
    app.run(debug=True)
