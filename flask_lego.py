from flask import Flask, render_template, request, flash
import rebrick
import json
import urllib.request
import urllib.error
import re


app = Flask(__name__)
app.secret_key = "super_secret_key"
app.jinja_env.filters['zip'] = zip


@app.route('/')
def index():
    flash("Podaj zestaw klocków LEGO.")
    return render_template('index.html')


@app.route('/sets', methods=['POST'])
def sets():
    num_format = re.compile(r'^[0-9][0-9]*$')
    rebrick.init("8e81bf52ab2d71baadb63847e48d5035")
    provided_lego_set = request.form['lego_set_input']
    it_is = re.match(num_format, provided_lego_set)
    if it_is:
        pass
    else:
        flash("Błąd! Podaj numer zestawu LEGO jeszcze raz")
        return render_template('index.html')
    try:
        response_name = rebrick.lego.get_set(provided_lego_set)
    except urllib.error.HTTPError as err:
        err.code
        flash("Nie ma takiego zestawu LEGO, spróbuj jeszcze raz")
        return render_template('index.html')

    response_name = rebrick.lego.get_set(provided_lego_set)
    response_sets = rebrick.lego.get_set_alternates(provided_lego_set)
    alternatives_sets = json.loads(response_sets.read())
    provided_lego_set_name = json.loads(response_name.read())

    if alternatives_sets.get('count') == 0:
        flash(
            f"""Brak alternatywnych zestawów dla: {provided_lego_set} - "{provided_lego_set_name['name']}" """)
        return render_template('index.html')
    else:
        img_set = []
        link_set = []
        for key, values in alternatives_sets.items():
            if key == 'results':
                for url in values:
                    img_set.append(url['moc_img_url'])
                    link_set.append(url['moc_url'])

        flash(
            f"""Alternatywne zestawy dla: {provided_lego_set} - "{provided_lego_set_name['name']}" """)
        return render_template('index.html', img_set=img_set, link_set=link_set)


if __name__ == "__main__":
    app.run()
