CREATE TABLE if not exists user_table(
    user_id integer PRIMARY KEY,
    username text,
    current_model text
);

-- TRUNCATE user_table;

-- INSERT INTO user_table
-- VALUES (42, 'lalala', 'PUSHKIN');


-- select * from user_table;

-- INSERT INTO user_table
-- VALUES (43, 'lololoshka', 'VOLK');


-- select * from user_table;

-- INSERT INTO user_table (user_id, username, current_model) 
-- VALUES (42, 'abc', 'VOLK')
-- ON CONFLICT (user_id)
-- DO 
--     UPDATE SET current_model = 'VOLK', username = 'abc';

-- select * from user_table;

-- create database cacti;

-- create table if not exists cacti_table (
--    family text,
--    subtype text,
--    spines_length integer
-- );

-- insert into cacti_table values ('rebutia', 'senilis', 3);
-- insert into cacti_table values ('rebutia', 'albiflora', 3);
-- insert into cacti_table values ('rebutia', 'miniscula', 1);
-- insert into cacti_table values ('echinopsis', 'amblayensis', 3);
-- insert into cacti_table values ('echinopsis', 'albispinosa', 4);
-- insert into cacti_table values ('mammillaria', 'bocasana', 4);


-- select * from cacti_table;