from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title, year FROM shows ORDER BY title;')


def get_most_rated_shows(offset, limit, sort_by, direction):
    query = f"""SELECT shows.id, title, year, runtime, rating, string_agg(name, ',' ORDER BY name) as genres,
            coalesce(trailer, 'NO URL') as trailer , coalesce(homepage, 'NO URL') as homepage
            FROM shows 
            LEFT JOIN show_genres on shows. id = show_genres.show_id
            LEFT JOIN genres on show_genres.genre_id=genres.id
			Group By shows.id
            ORDER BY {sort_by} {direction}
            LIMIT {limit} OFFSET {offset};"""

    return data_manager.execute_select(query)

def get_show_by_id(id):
    query = f"""
        SELECT s.id, title, year, runtime, rating, string_agg(g.name, ',' ORDER BY g.name) as genres, 
        overview, trailer 
        from shows s
        left join show_genres sg on s.id = sg.show_id
        left join genres g on sg.genre_id = g.id
        where s.id = {id}
        group by s.id
    """
    return data_manager.execute_select(query, fetchall=False)


def get_seasons_by_show_id(id):
    query = f"""
    SELECT  id, season_number, show_id, title, overview  
    from seasons 
    where show_id = {id}
    ORDER BY title
    """
    return data_manager.execute_select(query)


def get_actors_for_show(id):
    query = f"""
    select s.id, s.title, a.name, a.id as actor_id from
    actors a
    left join   show_characters sc on sc.actor_id = a.id
    left join shows s on s.id = sc.show_id
    where s.id = {id}
    limit 3
        """
    return data_manager.execute_select(query)


def get_number_of_shows():
    query = f"""
    SELECT COUNT(id) as num FROM shows
    """
    result = data_manager.execute_select(query, fetchall=False)
    return result['num']


def check_username(username):
    query = f"""
        SELECT EXISTS 
        (SELECT username from users
        WHERE username = %(username)s)
        """
    result = data_manager.execute_select(query, {"username" : username}, fetchall=False)
    return result['exists']


def register(username, password):
    query = f"""
                INSERT INTO users (username, password)
                VALUES (%(username)s, %(password)s )
                """
    data_manager.execute_dml_statement(query, {'username': username, 'password': password})


def get_password(username):
    query = f"""
        SELECT password from users
        WHERE username = %(username)s
        """
    result = data_manager.execute_select(query, {"username" : username}, fetchall=False)
    return result


def get_episodes(season_id):
    query = """
        SELECT e.id, e.title, episode_number, e.overview , s.title as "season_title", sh.title as "show_title", s.season_number as "season_number" 
        FROM episodes e
        LEFT JOIN seasons s on e.season_id = s.id
        LEFT JOIN shows sh on s.show_id = sh.id
        WHERE season_id = %(season_id)s
        ORDER BY  s.season_number, e.episode_number
        """
    result = data_manager.execute_select(query, {"season_id": int(season_id)})
    return result

def get_episode_length(episode_id):
    query= """
            SELECT episode_number 
            FROM episodes
            WHERE id = %(episode_id)s
            """
    result = data_manager.execute_select(query, {"episode_id" : int(episode_id)}, fetchall=False)
    return result


def get_actor_details(actor_id):
    query= """
            SELECT name, birthday, death, biography
            FROM actors 
            WHERE id = %(actor_id)s"""
    result = data_manager.execute_select(query, {"actor_id" : int(actor_id)}, fetchall=False)
    return result

def get_actor_genres(actor_id):
    query = """
        SELECT a.name, string_agg(g.name, ',') as gatunki
    FROM actors a 
    LEFT JOIN show_characters sc on a.id = sc.actor_id
    LEFT JOIN shows sh on sh.id = sc.show_id
    LEFT JOIN show_genres sg on sh.id = sg.show_id
    LEFT JOIN genres g on sg.genre_id = g.id
    WHERE a.id = %(actor_id)s
    GROUP BY a.name
    """
    result = data_manager.execute_select(query, {"actor_id" : int(actor_id)}, fetchall=False)
    return result

