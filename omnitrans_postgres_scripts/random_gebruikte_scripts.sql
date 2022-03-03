

DROP TABLE IF EXISTS eigenclips.bagpand_vldm_ruimextend;


CREATE TABLE public.links_geom AS




-- update links
UPDATE simple.link2_1data1
SET typenr = 20
WHERE linknr = 1366

--check
SELECT * FROM simple.link2_1data1 as a
WHERE a.linknr = 1366







--- om link lenth naar km te zetten.
UPDATE simple.link

SET length = length/1000






---update values in dimension table

UPDATE public.dimension





---- om tabel leeg te maken

SELECT * FROM simple.link5_2data1


TRUNCATE TABLE simple.link5_2data1
