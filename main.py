from flask import Flask, render_template, url_for
from data import queries

app = Flask('codecool_series')


@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)

@app.route('/shows/most-rated')
def most_rated_shows():
    most_rated = queries.most_rated_show()
    return render_template('most-rated.html', most_rated=most_rated)


@app.route('/tv-show/<int:id>')
@app.route('/tv-show/<int:id>/<season>')
def showinfos(id):
    show_details = queries.overview(id)
    show_seasons = queries.seasonoverview(id)
    return render_template('tv-shows.html', show_details=show_details, show_seasons=show_seasons)

@app.route('/design')
def design():
    return render_template('design.html')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
