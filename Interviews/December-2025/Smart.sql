--1

select name, distance,
        dense_rank() over(order by distance desc) as whichPlace
from result
order by name



--