DROP TABLE IF EXISTS public.links_omni_osmid;
CREATE TABLE public.links_omni_osmid as

SELECT  b.*, a.osmid

FROM public.point_where_flood_calculated as a
JOIN public.links_omnitrans_buffer2m as b
ON ST_Contains(b.geom, a.geom)
