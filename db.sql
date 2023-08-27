create table userRole
(
	id SERIAL primary key,
	description varchar(100) not null
);

create table userdb
(
	id SERIAL primary key,
	name varchar(500) not null,
	password varchar(120) not null,
	email varchar(200) unique not null,
	role int,
	constraint FK_role foreign key(role) references userRole(id)
);

create table portfolio
(
	id SERIAL primary key,
	ticker varchar(10) not null,
	price decimal(8,5) not null,
	volume int not null,
	userId int,
	constraint FK_userId foreign key(userId) references userdb(id)
);

insert into userRole(description) 
values ('admin') , ('user');