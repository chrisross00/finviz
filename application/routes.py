from flask import current_app as app
from flask import render_template



@app.route("/")
def home():
    """Landing page."""
    return render_template(
        "index.jinja2",
        title="FinViz420",
        description="aims to assist with stock selection by providing tools for fundamental and technical security analysis",
        template="home-template",
        body="This homepage is served with Flask."
    )