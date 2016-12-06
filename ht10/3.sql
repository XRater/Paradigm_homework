select City.Name from Country, City, Capital
where City.Id = Capital.CityId
and City.CountryCode = Country.Code
and Country.Name = "Malaysia";
