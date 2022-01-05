from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = '44237f3ba3449f5c0f8cc0bdb154b526'

from include import routes