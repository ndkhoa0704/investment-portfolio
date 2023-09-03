create table userRole
(
	id int identity(1,1)  primary key,
	description varchar(100) not null
);

create table userdb
(
	id int identity(1,1)  primary key,
	name varchar(500) not null,
	password varchar(120) not null,
	email varchar(200) unique not null,
	role int,
	constraint FK_role foreign key(role) references userRole(id)
);

create table portfolio
(
	id int identity(1,1)  primary key,
	ticker varchar(10) not null,
	price int not null,
	volume int not null,
	userid int,
	created_at datetime not null,
	constraint FK_userId foreign key(userId) references userdb(id)
);

insert into userRole(description) 
values ('admin') , ('user');