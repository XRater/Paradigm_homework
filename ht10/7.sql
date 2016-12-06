select Country.Name
from Country left outer join City on 
        CountryCode = Code
group by Code
having Country.Population > 2*sum(City.Population)
order by Country.Name;
