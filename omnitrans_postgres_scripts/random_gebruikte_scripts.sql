







--- om link lenth naar km te zetten.
UPDATE simple.link

SET length = length/1000






---update values in dimension table

UPDATE public.dimension





---- om tabel leeg te maken

SELECT * FROM simple.link5_2data1


TRUNCATE TABLE simple.link5_2data1
