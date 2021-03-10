
query = """
    SELECT e.title, episode_number, e.overview , s.title as "season title"
    FROM episodes e
    LEFT JOIN seasons s on e.season_id = s.id
    WHERE season_id = 3987
    ORDER BY  e.episode_number
"""

query= """
    SELECT COUNT(e.title) as "episodes num"
    FROM episodes e
    LEFT JOIN seasons s on e.season_id = s.id
    WHERE season_id = 3987
"""

query="""
    SELECT count(s.id) as num, sh.title
    FROM seasons s 
    LEFT JOIN shows sh on s.show_id = sh.id
    GROUP BY sh.title
    ORDER BY num DESC
    LIMIT 12
"""

query="""
    SELECT count(s.id) as num, sh.title, string_agg(s.title, ',')
    FROM seasons s 
    LEFT JOIN shows sh on s.show_id = sh.id
    
    WHERE sh.id = 1416
    GROUP BY sh.title
"""

query="""
    SELECT a.name, sh.title , sh.year, sh.rating
    FROM actors a
    LEFT JOIN show_characters sc ON a.id = sc.actor_id
    LEFT JOIN shows sh ON sc.show_id = sh.id
    WHERE a.name LIKE '%Cranston%'
"""

query="""
    SELECT a.name, sh.title , sh.year, sh.rating
    FROM actors a
    LEFT JOIN show_characters sc ON a.id = sc.actor_id
    LEFT JOIN shows sh ON sc.show_id = sh.id
"""

query = """
    SELECT a.name, sh.title
    FROM actors a
    LEFT JOIN show_characters sc ON a.id = sc.actor_id
    LEFT JOIN shows sh ON sc.show_id = sh.id
    WHERE a.birthday > '1970-01-01'
    AND sh.id = 1416
    """


query = '''
    SELECT a.name, string_agg(sh.title, ',')
    FROM actors a
    LEFT JOIN show_characters sc ON a.id = sc.actor_id
    LEFT JOIN shows sh ON sc.show_id = sh.id
    WHERE a.name LIKE '%Cranston%'
    GROUP BY a.name
'''

query = """
    SELECT string_agg(a.name, ','), e.title
    FROM actors a
    LEFT JOIN show_characters sc ON a.id = sc.actor_id
    LEFT JOIN shows sh ON sc.show_id = sh.id
    LEFT JOIN seasons s ON s.show_id = sh.id
    LEFT JOIN episodes e ON e.season_id = s.id
    WHERE e.id = 2247122
    GROUP BY e.title
"""

query="""
    SELECT a.name, string_agg(g.name, ',') as gatunki
FROM actors a 
LEFT JOIN show_characters sc on a.id = sc.actor_id
LEFT JOIN shows sh on sh.id = sc.show_id
LEFT JOIN show_genres sg on sh.id = sg.show_id
LEFT JOIN genres g on sg.genre_id = g.id
GROUP BY a.name
"""