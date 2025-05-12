from flask import Blueprint, request, render_template

test_bp = Blueprint('test', __name__)

@test_bp.route("/hello")
def hello():
    return render_template("hello.html", name="World")