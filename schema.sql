CREATE TABLE IF NOT EXISTS "generation_data" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "count" INTEGER NOT NULL,
    "min_length" INTEGER NOT NULL,
    "max_length" INTEGER NOT NULL,
    "arguments_parsing_time" REAL NOT NULL,
    "unary_generation_time" REAL NOT NULL,
    "whole_generation_time" REAL NOT NULL,
    "duplicates_count" INTEGER NOT NULL
);
CREATE TABLE sqlite_sequence(name,seq);
