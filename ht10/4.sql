select Country.Name, count(City.Name)
from Country left outer join City on Code = CountryCode
                and City.Population >= 1000000
group by Code
order by count(City.Name) desc, Country.Name;


