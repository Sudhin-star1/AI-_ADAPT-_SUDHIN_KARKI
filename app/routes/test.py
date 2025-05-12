from flask import Blueprint, request, render_template

# Create a test blueprint for test
test_bp = Blueprint('test', __name__)

# Route defined
@test_bp.route("/hello")
def hello():
    return render_template("hello.html", name="World")