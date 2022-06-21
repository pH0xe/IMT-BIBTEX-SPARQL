-------------------------------------------------------------
-- DATABASE
-------------------------------------------------------------
CREATE DATABASE "bibtex-project"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;




-------------------------------------------------------------
-- CREATE ROLE
-------------------------------------------------------------
CREATE ROLE "bibtex-user" WITH
  LOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  ENCRYPTED PASSWORD 'bibtex-user';

\c bibtex-project;




-------------------------------------------------------------
-- Grant admin right
-------------------------------------------------------------
GRANT ALL ON SCHEMA public TO PUBLIC;

GRANT ALL ON SCHEMA public TO postgres;




-------------------------------------------------------------
-- BIBFILE SEQUENCE
-------------------------------------------------------------
CREATE SEQUENCE IF NOT EXISTS public.bibfile_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.bibfile_id_seq
    OWNER TO postgres;

GRANT USAGE ON SEQUENCE public.bibfile_id_seq TO "bibtex-user";

GRANT ALL ON SEQUENCE public.bibfile_id_seq TO postgres;




-------------------------------------------------------------
-- BIBFILE TABLE
-------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.bibfile
(
    id integer NOT NULL DEFAULT nextval('bibfile_id_seq'::regclass),
    uploaddate bigint NOT NULL,
    name character(250) COLLATE pg_catalog."default" NOT NULL,
    data bytea NOT NULL,
    size bigint NOT NULL,
    contenttype character(250) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT bibfile_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.bibfile
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE public.bibfile TO "bibtex-user";

GRANT ALL ON TABLE public.bibfile TO postgres;




-------------------------------------------------------------
-- REGISTERUSER SEQUENCE
-------------------------------------------------------------
CREATE SEQUENCE IF NOT EXISTS public.registeruser_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.registeruser_id_seq
    OWNER TO postgres;

GRANT USAGE ON SEQUENCE public.registeruser_id_seq TO "bibtex-user";

GRANT ALL ON SEQUENCE public.registeruser_id_seq TO postgres;




-------------------------------------------------------------
-- REGISTERUSER TABLE
-------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.registeruser
(
    id integer NOT NULL DEFAULT nextval('registeruser_id_seq'::regclass),
    login character varying(250) COLLATE pg_catalog."default" NOT NULL,
    password character varying(1000) COLLATE pg_catalog."default" NOT NULL,
    superadmin boolean NOT NULL,
    CONSTRAINT user_pkey PRIMARY KEY (id),
    CONSTRAINT c1_unique_login UNIQUE (login)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.registeruser
    OWNER to postgres;

GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE public.registeruser TO "bibtex-user";

GRANT ALL ON TABLE public.registeruser TO postgres;
