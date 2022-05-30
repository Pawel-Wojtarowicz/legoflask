from os import link
from flask import Flask, render_template, request, flash, jsonify
import rebrick
import json

app = Flask(__name__)
app.secret_key = "super_secret_key"
app.jinja_env.filters['zip'] = zip


@app.route('/')
def index():
    flash("Podaj zestaw klocków LEGO.")
    return render_template('index.html')


@app.route('/sets', methods=['POST'])
def sets():
    rebrick.init("8e81bf52ab2d71baadb63847e48d5035")
    provided_lego_set = request.form['lego_set_input']
    response_sets = rebrick.lego.get_set_alternates(provided_lego_set)
    response_name = rebrick.lego.get_set(provided_lego_set)
    alternatives_sets = json.loads(response_sets.read())
    provided_lego_set_name = json.loads(response_name.read())

    img_set = []
    link_set = []
    for key, values in alternatives_sets.items():
        if key == 'results':
            for url in values:
                img_set.append(url['moc_img_url'])
                link_set.append(url['moc_url'])

    flash(
        f"Alternatywne zestawy dla: {provided_lego_set} - {provided_lego_set_name['name']}")
    return render_template('index.html', img_set=img_set, link_set=link_set)
