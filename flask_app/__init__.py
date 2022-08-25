from flask import Flask, render_template, redirect, request, session, flash
from flask_mail import Mail
from dotenv import load_dotenv
import os
f'{os.getenv("SECRET_KEY")}'

from flask_bcrypt import Bcrypt      

app = Flask(__name__)
mail = Mail(app)

app.secret_key = f'{os.getenv("SECRET_KEY")}'
bcrypt = Bcrypt(app)

load_dotenv()