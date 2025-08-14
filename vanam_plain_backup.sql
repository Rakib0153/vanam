--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

-- Started on 2025-08-05 13:35:06

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 216 (class 1259 OID 107121)
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    phone character varying(20) NOT NULL,
    email character varying(100),
    "position" character varying(100),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 107120)
-- Name: employees_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employees_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employees_id_seq OWNER TO postgres;

--
-- TOC entry 4934 (class 0 OID 0)
-- Dependencies: 215
-- Name: employees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employees_id_seq OWNED BY public.employees.id;


--
-- TOC entry 226 (class 1259 OID 107232)
-- Name: help_slips; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.help_slips (
    id integer NOT NULL,
    employee_id integer,
    title character varying(255) NOT NULL,
    description text NOT NULL,
    priority character varying(20) DEFAULT 'Medium'::character varying,
    contact_info character varying(100),
    status character varying(50) DEFAULT 'Request Submitted'::character varying,
    assigned_to integer,
    remarks text,
    resolved_by integer,
    resolve_date timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    tat_hours numeric(10,2)
);


ALTER TABLE public.help_slips OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 107231)
-- Name: help_slips_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.help_slips_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.help_slips_id_seq OWNER TO postgres;

--
-- TOC entry 4935 (class 0 OID 0)
-- Dependencies: 225
-- Name: help_slips_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.help_slips_id_seq OWNED BY public.help_slips.id;


--
-- TOC entry 224 (class 1259 OID 107189)
-- Name: performance_scores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.performance_scores (
    id integer NOT NULL,
    employee_id integer,
    task_completion_score integer DEFAULT 0,
    timeliness_score integer DEFAULT 0,
    quality_score integer DEFAULT 0,
    last_updated timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.performance_scores OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 107188)
-- Name: performance_scores_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.performance_scores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.performance_scores_id_seq OWNER TO postgres;

--
-- TOC entry 4936 (class 0 OID 0)
-- Dependencies: 223
-- Name: performance_scores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.performance_scores_id_seq OWNED BY public.performance_scores.id;


--
-- TOC entry 228 (class 1259 OID 107263)
-- Name: task_reviews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task_reviews (
    id integer NOT NULL,
    task_id integer,
    rating integer,
    comments text,
    reviewer_id integer,
    created_at timestamp without time zone
);


ALTER TABLE public.task_reviews OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 107262)
-- Name: task_reviews_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.task_reviews_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_reviews_id_seq OWNER TO postgres;

--
-- TOC entry 4937 (class 0 OID 0)
-- Dependencies: 227
-- Name: task_reviews_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.task_reviews_id_seq OWNED BY public.task_reviews.id;


--
-- TOC entry 222 (class 1259 OID 107169)
-- Name: task_updates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task_updates (
    id integer NOT NULL,
    task_id integer,
    update_text text NOT NULL,
    status character varying(50) NOT NULL,
    updated_by integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.task_updates OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 107168)
-- Name: task_updates_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.task_updates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_updates_id_seq OWNER TO postgres;

--
-- TOC entry 4938 (class 0 OID 0)
-- Dependencies: 221
-- Name: task_updates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.task_updates_id_seq OWNED BY public.task_updates.id;


--
-- TOC entry 220 (class 1259 OID 107146)
-- Name: tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    assigned_to integer,
    assigned_by integer,
    status character varying(50) DEFAULT 'Pending'::character varying,
    priority character varying(20) DEFAULT 'Medium'::character varying,
    deadline date,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.tasks OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 107145)
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tasks_id_seq OWNER TO postgres;

--
-- TOC entry 4939 (class 0 OID 0)
-- Dependencies: 219
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- TOC entry 218 (class 1259 OID 107133)
-- Name: team_leaders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.team_leaders (
    id integer NOT NULL,
    employee_id integer,
    department character varying(100),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.team_leaders OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 107132)
-- Name: team_leaders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.team_leaders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.team_leaders_id_seq OWNER TO postgres;

--
-- TOC entry 4940 (class 0 OID 0)
-- Dependencies: 217
-- Name: team_leaders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.team_leaders_id_seq OWNED BY public.team_leaders.id;


--
-- TOC entry 4718 (class 2604 OID 107124)
-- Name: employees id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees ALTER COLUMN id SET DEFAULT nextval('public.employees_id_seq'::regclass);


--
-- TOC entry 4734 (class 2604 OID 107235)
-- Name: help_slips id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.help_slips ALTER COLUMN id SET DEFAULT nextval('public.help_slips_id_seq'::regclass);


--
-- TOC entry 4729 (class 2604 OID 107192)
-- Name: performance_scores id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.performance_scores ALTER COLUMN id SET DEFAULT nextval('public.performance_scores_id_seq'::regclass);


--
-- TOC entry 4739 (class 2604 OID 107266)
-- Name: task_reviews id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_reviews ALTER COLUMN id SET DEFAULT nextval('public.task_reviews_id_seq'::regclass);


--
-- TOC entry 4727 (class 2604 OID 107172)
-- Name: task_updates id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_updates ALTER COLUMN id SET DEFAULT nextval('public.task_updates_id_seq'::regclass);


--
-- TOC entry 4722 (class 2604 OID 107149)
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- TOC entry 4720 (class 2604 OID 107136)
-- Name: team_leaders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team_leaders ALTER COLUMN id SET DEFAULT nextval('public.team_leaders_id_seq'::regclass);


--
-- TOC entry 4916 (class 0 OID 107121)
-- Dependencies: 216
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employees (id, name, phone, email, "position", created_at) FROM stdin;
9	Rakib	+919083480153	ri299850@gmail.com	Data Analyst or Mis	2025-08-02 15:33:20.670515
11	Nikita	+1222333444	nikita@gmail.com	Team Leader	2025-08-02 15:33:20.670515
10	Raju	+919163041321	raju@gmail.com	Accountant	2025-08-02 15:33:20.670515
12	Uma Yadav	+918017255804	uma@gmail.com	Fornt Desk	2025-08-04 14:46:51.085761
\.


--
-- TOC entry 4926 (class 0 OID 107232)
-- Dependencies: 226
-- Data for Name: help_slips; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.help_slips (id, employee_id, title, description, priority, contact_info, status, assigned_to, remarks, resolved_by, resolve_date, created_at, updated_at, tat_hours) FROM stdin;
\.


--
-- TOC entry 4924 (class 0 OID 107189)
-- Dependencies: 224
-- Data for Name: performance_scores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.performance_scores (id, employee_id, task_completion_score, timeliness_score, quality_score, last_updated) FROM stdin;
6	10	100	100	80	2025-08-02 16:24:24.911828
7	11	0	0	0	2025-08-04 11:43:28.750198
8	12	0	0	0	2025-08-04 15:11:16.352266
5	9	50	100	20	2025-08-02 15:58:48.371447
\.


--
-- TOC entry 4928 (class 0 OID 107263)
-- Dependencies: 228
-- Data for Name: task_reviews; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task_reviews (id, task_id, rating, comments, reviewer_id, created_at) FROM stdin;
1	4	1	Not Good 	5	2025-08-04 07:02:03.445938
\.


--
-- TOC entry 4922 (class 0 OID 107169)
-- Dependencies: 222
-- Data for Name: task_updates; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task_updates (id, task_id, update_text, status, updated_by, created_at) FROM stdin;
5	4	now pending	Pending	9	2025-08-02 15:58:12.978319
6	4	stage 2\r\n	In Progress	9	2025-08-02 15:58:26.870446
7	4	stage 3	In Progress	9	2025-08-02 15:58:38.025308
8	4	yea	Completed	9	2025-08-02 15:58:48.36455
9	5	s	In Progress	10	2025-08-02 18:01:49.152034
10	5	s	In Progress	10	2025-08-02 18:01:50.996117
11	5	a	Pending	10	2025-08-02 18:02:04.989834
12	5	qw	Completed	10	2025-08-02 18:02:18.142555
13	6	s	In Progress	9	2025-08-03 16:06:56.826964
15	13	working on	In progress	9	2025-08-04 14:12:20.777172
16	13	working on	Completed	9	2025-08-04 14:12:59.691225
17	14	i need time	Pending	10	2025-08-04 14:52:51.929134
18	14	i need time	In progress	10	2025-08-04 14:55:08.586594
19	15	stage 1	In progress	12	2025-08-04 15:03:30.40218
\.


--
-- TOC entry 4920 (class 0 OID 107146)
-- Dependencies: 220
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tasks (id, title, description, assigned_to, assigned_by, status, priority, deadline, created_at, updated_at) FROM stdin;
4	Make a Mis Help Slip	Now it imlot	9	5	Completed	High	2025-08-02	2025-08-02 15:42:35.081896	2025-08-02 15:58:48.36455
5	Check the account and told me how it was happen	ad	10	5	Completed	High	2025-08-03	2025-08-02 15:43:19.171142	2025-08-02 18:02:18.142555
6	new tasl	hh	9	5	In Progress	Medium	2025-08-03	2025-08-03 15:56:59.442526	2025-08-03 16:06:56.826964
7	Create a Help slip 	Where the employees can give response 	9	5	Pending	Medium	2025-08-04	2025-08-04 12:34:02.261599	2025-08-04 12:34:02.261599
13	Check the whatsapp collecter	it was working fine or not	9	5	Completed	High	2025-08-04	2025-08-04 14:11:54.817337	2025-08-04 08:42:59.693196
14	Check invoice 	Now	10	5	In progress	High	2025-08-04	2025-08-04 14:51:21.675218	2025-08-04 09:25:08.588884
15	entry todays packs	it was need by naman sir 	12	5	In progress	High	2025-08-04	2025-08-04 14:59:09.076581	2025-08-04 09:33:30.404641
16	demo12	12	12	5	Pending	Medium	2025-08-04	2025-08-04 15:50:27.870588	2025-08-04 15:50:27.870588
\.


--
-- TOC entry 4918 (class 0 OID 107133)
-- Dependencies: 218
-- Data for Name: team_leaders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.team_leaders (id, employee_id, department, created_at) FROM stdin;
5	11	MD and Team Leader	2025-08-02 15:34:02.153331
\.


--
-- TOC entry 4941 (class 0 OID 0)
-- Dependencies: 215
-- Name: employees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employees_id_seq', 12, true);


--
-- TOC entry 4942 (class 0 OID 0)
-- Dependencies: 225
-- Name: help_slips_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.help_slips_id_seq', 1, false);


--
-- TOC entry 4943 (class 0 OID 0)
-- Dependencies: 223
-- Name: performance_scores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.performance_scores_id_seq', 8, true);


--
-- TOC entry 4944 (class 0 OID 0)
-- Dependencies: 227
-- Name: task_reviews_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_reviews_id_seq', 1, true);


--
-- TOC entry 4945 (class 0 OID 0)
-- Dependencies: 221
-- Name: task_updates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_updates_id_seq', 19, true);


--
-- TOC entry 4946 (class 0 OID 0)
-- Dependencies: 219
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tasks_id_seq', 16, true);


--
-- TOC entry 4947 (class 0 OID 0)
-- Dependencies: 217
-- Name: team_leaders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.team_leaders_id_seq', 5, true);


--
-- TOC entry 4741 (class 2606 OID 107131)
-- Name: employees employees_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_email_key UNIQUE (email);


--
-- TOC entry 4743 (class 2606 OID 107129)
-- Name: employees employees_phone_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_phone_key UNIQUE (phone);


--
-- TOC entry 4745 (class 2606 OID 107127)
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- TOC entry 4755 (class 2606 OID 107243)
-- Name: help_slips help_slips_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.help_slips
    ADD CONSTRAINT help_slips_pkey PRIMARY KEY (id);


--
-- TOC entry 4753 (class 2606 OID 107198)
-- Name: performance_scores performance_scores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.performance_scores
    ADD CONSTRAINT performance_scores_pkey PRIMARY KEY (id);


--
-- TOC entry 4760 (class 2606 OID 107270)
-- Name: task_reviews task_reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_reviews
    ADD CONSTRAINT task_reviews_pkey PRIMARY KEY (id);


--
-- TOC entry 4751 (class 2606 OID 107177)
-- Name: task_updates task_updates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_updates
    ADD CONSTRAINT task_updates_pkey PRIMARY KEY (id);


--
-- TOC entry 4749 (class 2606 OID 107157)
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- TOC entry 4747 (class 2606 OID 107139)
-- Name: team_leaders team_leaders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team_leaders
    ADD CONSTRAINT team_leaders_pkey PRIMARY KEY (id);


--
-- TOC entry 4756 (class 1259 OID 107261)
-- Name: idx_help_slip_assigned; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_help_slip_assigned ON public.help_slips USING btree (assigned_to);


--
-- TOC entry 4757 (class 1259 OID 107260)
-- Name: idx_help_slip_employee; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_help_slip_employee ON public.help_slips USING btree (employee_id);


--
-- TOC entry 4758 (class 1259 OID 107259)
-- Name: idx_help_slip_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_help_slip_status ON public.help_slips USING btree (status);


--
-- TOC entry 4767 (class 2606 OID 107249)
-- Name: help_slips help_slips_assigned_to_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.help_slips
    ADD CONSTRAINT help_slips_assigned_to_fkey FOREIGN KEY (assigned_to) REFERENCES public.employees(id) ON DELETE SET NULL;


--
-- TOC entry 4768 (class 2606 OID 107244)
-- Name: help_slips help_slips_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.help_slips
    ADD CONSTRAINT help_slips_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(id) ON DELETE CASCADE;


--
-- TOC entry 4769 (class 2606 OID 107254)
-- Name: help_slips help_slips_resolved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.help_slips
    ADD CONSTRAINT help_slips_resolved_by_fkey FOREIGN KEY (resolved_by) REFERENCES public.employees(id) ON DELETE SET NULL;


--
-- TOC entry 4766 (class 2606 OID 107199)
-- Name: performance_scores performance_scores_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.performance_scores
    ADD CONSTRAINT performance_scores_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(id) ON DELETE CASCADE;


--
-- TOC entry 4770 (class 2606 OID 107276)
-- Name: task_reviews task_reviews_reviewer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_reviews
    ADD CONSTRAINT task_reviews_reviewer_id_fkey FOREIGN KEY (reviewer_id) REFERENCES public.team_leaders(id);


--
-- TOC entry 4771 (class 2606 OID 107271)
-- Name: task_reviews task_reviews_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_reviews
    ADD CONSTRAINT task_reviews_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


--
-- TOC entry 4764 (class 2606 OID 107178)
-- Name: task_updates task_updates_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_updates
    ADD CONSTRAINT task_updates_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id) ON DELETE CASCADE;


--
-- TOC entry 4765 (class 2606 OID 107183)
-- Name: task_updates task_updates_updated_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_updates
    ADD CONSTRAINT task_updates_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES public.employees(id) ON DELETE SET NULL;


--
-- TOC entry 4762 (class 2606 OID 107163)
-- Name: tasks tasks_assigned_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_assigned_by_fkey FOREIGN KEY (assigned_by) REFERENCES public.team_leaders(id) ON DELETE SET NULL;


--
-- TOC entry 4763 (class 2606 OID 107158)
-- Name: tasks tasks_assigned_to_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_assigned_to_fkey FOREIGN KEY (assigned_to) REFERENCES public.employees(id) ON DELETE SET NULL;


--
-- TOC entry 4761 (class 2606 OID 107140)
-- Name: team_leaders team_leaders_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team_leaders
    ADD CONSTRAINT team_leaders_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(id) ON DELETE CASCADE;


-- Completed on 2025-08-05 13:35:06

--
-- PostgreSQL database dump complete
--

