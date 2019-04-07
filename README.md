# Reporting Tool Program

This reporting tool analyzes data in a news website database to answer the following questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Getting Started

### Prerequisites

* Python interpreter
* PostgreSQL
* News data
* Psycopg2 (run command: *pip install psycopg2*)

### Installing

1. Verify all prerequisites are installed
2. Verify the newsdatadb.py file is in the same folder as the newsdata.sql file
3. Navigate to their shared folder in your command prompt
4. To connect to the database, run command: *psql news*
5. To set up necessary views, run the following commands:

```
create view articles_log as select articles.author, count(log.id) from articles join log on articles.slug = replace(log.path,'/article/','') group by articles.author order by count(log.id) desc;

create view error_log as select time::date, count(status) from log where status = '404 NOT FOUND' group by time::date order by count(status) desc;

create view status_log as select time::date, count(status) from log group by time::date order by count(status) desc;

create view error_rate as select status_log.time, cast(error_log.count as decimal) / status_log.count * 100 as result from status_log left join error_log on status_log.time = error_log.time order by result desc;
```

6. To disconnect from the database, run command: *\q*
7. To run the program, run command: *python newsdatadb.py*
8. View report results in command prompt

## Code Design

### Problem One: What are the most popular three articles of all time?

1. SELECT logs per article title from articles + log

### Problem Two: Who are the most popular article authors of all time?

1. CREATE VIEW for logs per author ID from articles + log
2. SELECT logs per author name from authors + articles_log

### Problem Three: On which days did more than 1% of requests lead to errors?

1. CREATE VIEW for # errors per date from log
2. CREATE VIEW for total # requests per date from log
3. CREATE VIEW for % errors per date from error_log + status_log
4. SELECT % errors > 1% from error_rate

## Built With

* [Python](https://www.python.org/downloads/) - Programming language
* [PostgreSQL](https://www.postgresql.org/) - Database
* [Vagrant](https://www.vagrantup.com/) - Virtual machine management
* [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) - Runs virtual machine

## Authors

* **Sara Neel** - [sneelz](https://github.com/sneelz)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks Udacity!
