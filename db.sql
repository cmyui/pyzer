create table user_statistics
(
	id integer not null,
	mode integer not null,
	pp double precision default 0.0 not null,
	global_rank integer,
	country_rank integer,
	hit_accuracy double precision default 0.0 not null,
	play_count integer default 0 not null,
	play_time integer default 0 not null,
	total_score integer default 0 not null,
	total_hits integer default 0 not null,
	maximum_combo integer default 0 not null,
	replays_watched_by_others integer default 0 not null,
	is_ranked boolean default false not null,
	ranked_score integer default 0 not null,
	constraint user_statistics_pk
		primary key (id, mode)
);

alter table user_statistics owner to postgres;

create table user_relations
(
	id serial not null
		constraint user_relations_pk
			primary key,
	user_a integer not null,
	user_b integer not null,
	blocked boolean not null,
	created_at time default now() not null
);

alter table user_relations owner to postgres;

create unique index user_relations_id_uindex
	on user_relations (id);

create table seasonal_backgrounds
(
	id serial not null
		constraint seasonal_backgrounds_pk
			primary key,
	url varchar(2048) not null,
	creator_id integer not null
);

alter table seasonal_backgrounds owner to postgres;

create unique index seasonal_backgrounds_id_uindex
	on seasonal_backgrounds (id);

create table users
(
	id serial not null,
	username varchar(32),
	join_date timestamp with time zone,
	last_visit timestamp with time zone,
	country_code char(2),
	profile_colour char(7),
	privileges integer,
	pm_friends_only boolean,
	twitter varchar(15),
	discord varchar(37),
	website varchar(2048),
	follower_count integer,
	mapping_follower_count integer,
	max_friends integer,
	max_blocks integer,
	hashed_password char(60) not null,
	is_bot boolean default false not null,
	is_supporter boolean default false not null,
	has_supported boolean default false not null,
	interests varchar(30) default NULL::character varying,
	kudosu_total integer default 0 not null,
	kudosu_available integer default 0 not null,
	location varchar(30) default NULL::character varying,
	occupation varchar(30) default NULL::character varying,
	title varchar(128) default NULL::character varying
);

alter table users owner to postgres;
