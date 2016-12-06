select Name, Rate from Country, LiteracyRate
where Code = LiteracyRate.CountryCode
group by CountryCode
having Year = max(Year)
order by Rate desc limit 1;
