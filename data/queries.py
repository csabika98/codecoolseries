from data import data_manager
import data


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def most_rated_show():
    return data_manager.execute_select("""SELECT shows.id, shows.title, shows.homepage, shows.year as year, shows.runtime as runtime, shows.trailer as trailer,shows.rating as rating, array_agg(genres.name) as genres
                FROM shows
                LEFT JOIN show_genres on shows.id = show_genres.show_id
                INNER JOIN genres on show_genres.genre_id = genres.id
                GROUP BY shows.id
                ORDER BY rating DESC
                LIMIT 15;""")