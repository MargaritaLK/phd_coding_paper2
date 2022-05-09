
----- sample verise 1---

DROP TABLE IF EXISTS public.links_omni_osmid2;
CREATE TABLE public.links_omni_osmid2 as

SELECT  b.* , a.arrivaltime, a.minutes, a.osmid, a.maaiveld

FROM public.df_arrival_segments as a
JOIN public.links_omni_buffer4m as b
ON ST_Contains(b.geom, a.geom)



---------
---sample versie twee, met grote sample size
------

---steps--



DROP TABLE IF EXISTS public.links_omni_flood_scen1;
CREATE TABLE public.links_omni_flood_scen1 as

SELECT  b.* , a.arrivaltime, a.min_int as minutes, a.osmid, a.maaiveld

FROM public.segments_sample2_scen1 as a
JOIN public.links_omni_buffer4m as b
ON ST_Contains(b.geom, a.geom)

WHERE b.roadtypeab != 'Connector'





--- voor scen 1 en 2

DROP TABLE IF EXISTS public.links_omni_flood_uuid28d3_scen2_n9corr;
CREATE TABLE public.links_omni_flood_uuid28d3_scen2_n9corr as

SELECT  b.* , a.arrivaltime, a.min_int as minutes, a.osmid, a.maaiveld

FROM public.segments_uuid28d3_scen2_n9corr as a
JOIN public.links_omni_buffer4m as b
ON ST_Contains(b.geom, a.geom)

WHERE b.roadtypeab != 'Connector'
