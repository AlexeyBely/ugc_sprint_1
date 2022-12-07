CREATE DATABASE movies;

CREATE DATABASE shard;

CREATE DATABASE replica;

CREATE TABLE shard.frames (
	`id` Int64,
    `user_id` String,
    `movie_id` String,
    `frame` Int32,
    `event_time` DateTime
) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/frames', 'replica_1')
PARTITION BY toYYYYMMDD(event_time)
ORDER BY id;

CREATE TABLE replica.frames (
	`id` Int64,
    `user_id` String,
    `movie_id` String,
    `frame` Int32,
    `event_time` DateTime
) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/frames', 'replica_2')
PARTITION BY toYYYYMMDD(event_time)
ORDER BY id;

CREATE TABLE movies.frames (
	`id` Int64,
    `user_id` String,
    `movie_id` String,
    `frame` Int32,
    `event_time` DateTime
) ENGINE = Distributed('company_cluster', '', frames, rand());