create table website (uuid varchar(64) primary key, website varchar(1024), py varchar(256), inputcode varchar(32))
create table namepwd (uuid varchar(64) primary key, websiteid int, name varchar(1024), val varchar(1024), seq int)
create table rsa(uuid varchar(64) primary key, pub varchar(4096), priv varchar(4096))