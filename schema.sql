CREATE TABLE IF NOT EXISTS "generation_data" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "count" INTEGER NOT NULL,
    "min_length" INTEGER NOT NULL,
    "max_length" INTEGER NOT NULL,
    "arguments_parsing_time" REAL NOT NULL,
    "unary_generation_time" REAL NOT NULL,
    "whole_generation_time" REAL NOT NULL,
    "duplicates_count" INTEGER NOT NULL,
	"c_files_hash" TEXT,
	"py_files_hash" TEXT,
	"git_commit_message" TEXT
);

CREATE VIEW IF NOT EXISTS
"rating" AS
select count,
whole_generation_time,
max_length,
(max_length - min_length),
c_files_hash, py_files_hash,
git_commit_message
from generation_data
where whole_generation_time > 1
order by
-whole_generation_time, -count,
min_length;

CREATE VIEW IF NOT EXISTS
"useful_data" AS
select
whole_generation_time, count,
max_length, c_files_hash,
py_files_hash, git_commit_message 
from generation_data
order by -whole_generation_time;

CREATE VIEW IF NOT EXISTS
"time_cost_calculations" AS
select * from useful_data
where whole_generation_time > 1;