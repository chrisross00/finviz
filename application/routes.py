from flask import current_app as app
from flask import render_template



@app.route("/")
def home():
    """Landing page."""
    return render_template(
        "index.jinja2",
        title="FinViz, a Plotly Dash App within Flask",
        description="a data visualizer for assisting with financial assessments",
        template="home-template",
        body="This homepage is served with Flask."
    )
    