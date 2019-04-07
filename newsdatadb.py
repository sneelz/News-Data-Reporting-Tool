#!/usr/bin/env python

import psycopg2

DBNAME = "news"

##############################################################
# PROBLEM ONE


def problem_one():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    # Join articles with log for logs per article title:
    c.execute('''
    select articles.title, cast(count(log.id) as int)
    from articles join log on articles.slug = replace(log.path,'/article/','')
    group by articles.title
    order by count(log.id) desc
    limit 3;
    ''')

    rows = c.fetchall()
    for row in rows:
        print("\"{}\" - {} views".format(row[0], row[1]))
    db.close()


##############################################################
# PROBLEM TWO

# CREATE VIEW
# create view articles_log as select articles.author, count(log.id)
# from articles join log on articles.slug = replace(log.path,'/article/','')
# group by articles.author
# order by count(log.id) desc;

def problem_two():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    # Join authors with articles_log for logs per author name:
    c.execute('''
    select authors.name, cast(articles_log.count as int)
    from authors join articles_log on authors.id = articles_log.author
    order by count desc;
    ''')

    rows = c.fetchall()
    for row in rows:
        print("{} - {} views".format(row[0], row[1]))
    db.close()


##############################################################
# PROBLEM THREE

# CREATE VIEW
# create view error_log as select time::date, count(status)
# from log where status = '404 NOT FOUND'
# group by time::date
# order by count(status) desc;

# CREATE VIEW
# create view status_log as select time::date, count(status)
# from log group by time::date
# order by count(status) desc;

# CREATE VIEW
# create view error_rate as select status_log.time,
# cast(error_log.count as decimal) / status_log.count * 100 as result
# from status_log left join error_log on status_log.time = error_log.time
# order by result desc;

def problem_three():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    # Select only results where % error > 1:
    c.execute("select * from error_rate where error_rate.result > 1;")

    rows = c.fetchall()
    for row in rows:
        print("{} - {}% errors".format(row[0], round(row[1], 2)))
    db.close()


##############################################################
# CALL FUNCTIONS

print('\nWhat are the most popular three articles of all time?')
print('-------------------------------------------------------')
problem_one()

print('\nWho are the most popular article authors of all time?')
print('-------------------------------------------------------')
problem_two()

print('\nOn which days did more than 1% of requests lead to errors?')
print('-------------------------------------------------------')
problem_three()

print('\n')
