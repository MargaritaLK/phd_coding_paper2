
DROP TABLE IF EXISTS public.links_omni_osmid2;
CREATE TABLE public.links_omni_osmid2 as

SELECT  b.* , a.arrivaltime, a.minutes, a.osmid, a.maaiveld

FROM public.df_arrival_segments as a
JOIN public.links_omni_buffer4m as b
ON ST_Contains(b.geom, a.geom)
