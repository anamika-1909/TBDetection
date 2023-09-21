from flask import Blueprint,render_template, request,redirect
from app import db
from flask_login import login_required, current_user
# from models import EditAccountForm
# from models import current_user
main = Blueprint('main', __name__)

@main.route('/')
def index1():
    return render_template('index1.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html',name=current_user.name,firstname=current_user.firstname,lastname=current_user.lastname,age=current_user.age,bp=current_user.bp,bs=current_user.bs,cough=current_user.cough,pasttb=current_user.pasttb,weight=current_user.weight)


@main.route('/abouttb')
# @login_required
def abouttb():
    return render_template('abouttb.html')

