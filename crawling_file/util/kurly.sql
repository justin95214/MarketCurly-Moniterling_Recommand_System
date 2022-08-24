create table daduckDB.pear(
    date datetime,
    title varchar(500),
    price int,
    weight varchar(500),
    kind varchar(500),
    site varchar(500),
    location varchar(500)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
alter table daduckDB.naver add primary key(date, title, price);

create table daduckDB.pear(
    date datetime,
    title varchar(500),
    price int,
    weight varchar(500),
    kind varchar(500),
    site varchar(500),
    location varchar(500)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
alter table daduckDB.gmarket add primary key(date, title, price);

create table daduckDB.coupang (
    date datetime,
    title varchar(500),
    price int,
    weight varchar(500),
    kind varchar(500),
    site varchar(500),
    location varchar(500)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
alter table daduckDB.coupang add primary key(date, title, price);

create table daduckDB.emart (
    date datetime,
    title varchar(500),
    price int,
    weight varchar(500),
    kind varchar(500),
    site varchar(500),
    location varchar(500)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
alter table daduckDB.emart add primary key(date, title, price);

create table daduckDB.Total (
    date datetime,
    title varchar(500),
    price int,
    weight varchar(500),
    kind varchar(500),
    site varchar(500),
    location varchar(500)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
alter table daduckDB.Total add primary key(date, title, price);

/*select * FROM daduckDB.naver Limit 2000;*/
