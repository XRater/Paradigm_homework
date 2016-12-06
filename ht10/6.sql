select City.Name, City.Population, Country.Population
from Country left outer join City on 
        CountryCode = Code
group by Code
order by City.Population/Country.Population desc, City.Name desc limit(20);


