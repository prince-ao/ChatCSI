from flask import Blueprint, render_template

view_bp = Blueprint("view", __name__, template_folder="templates")


@view_bp.route('/')
def index():
    return render_template("home/index.html", chat_url="/api/chat-general")


@view_bp.route('/admissions')
def admissions():
    return render_template("admissions/index.html", chat_url="/api/chat-admissions")


@view_bp.route('/cs')
def cs():
    return render_template("cs/index.html", chat_url="/api/chat-cs")
