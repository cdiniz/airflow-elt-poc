SELECT data #>> '{Country}' as country, 
                             day,
                             sum((data #>> '{Confirmed}')::int) as confirmed,
                             sum((data #>> '{Deaths}')::int) as deaths,
                             sum((data #>> '{Recovered}')::int) as recovered,   
                             sum((data #>> '{Active}')::int) as active
                      FROM covid19
                      GROUP BY country, day
