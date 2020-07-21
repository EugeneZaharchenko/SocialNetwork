from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

import views
