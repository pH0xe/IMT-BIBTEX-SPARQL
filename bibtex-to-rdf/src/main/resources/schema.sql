-- DROP TABLE IF EXISTS public.bibfile;

CREATE TABLE IF NOT EXISTS public.bibfile
(
    id integer NOT NULL DEFAULT nextval('bibfile_id_seq'::regclass),
    uploaddate bigint NOT NULL,
    name character(250) COLLATE pg_catalog."default" NOT NULL,
    data oid NOT NULL,
    size bigint NOT NULL,
    contenttype character(250) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT bibfile_pkey PRIMARY KEY (id)
)