create table kurly.naver (
    date datetime,
    title varchar(500),
    price int,
    weight varchar(500),
    kind varchar(500),
    site varchar(500),
    location varchar(500)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
alter table kurly.naver add primary key(date, title, price);

create table kurly.gmarket (
    date datetime,
    title varchar(500),
    price int,
    weight varchar(500),
    kind varchar(500),
    site varchar(500),
    location varchar(500)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
alter table kurly.gmarket add primary key(date, title, price);

create table kurly.coupang (
    date datetime,
    title varchar(500),
    price int,
    weight varchar(500),
    kind varchar(500),
    site varchar(500),
    location varchar(500)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
alter table kurly.coupang add primary key(date, title, price);

create table kurly.emart (
    date datetime,
    title varchar(500),
    price int,
    weight varchar(500),
    kind varchar(500),
    site varchar(500),
    location varchar(500)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
alter table kurly.emart add primary key(date, title, price);

/*select * FROM kurly.naver Limit 2000;*/