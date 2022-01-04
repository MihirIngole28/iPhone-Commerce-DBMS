create table F21_S001_2_Outlet(
Outlet_id		varchar(8)	not null ,
City			char(15)	not null ,
State			char(15)	not null ,
primary key (Outlet_id)
);


create table F21_S001_2_Warehouse(
Warehouse_id		varchar(8)	not null ,
primary key(Warehouse_id),
foreign key(Warehouse_id) references F21_S001_2_Outlet(Outlet_id)
on delete cascade
);


create table F21_S001_2_Store(
Store_id		varchar(8)	not null ,
primary key(Store_id),
foreign key(Store_id) references F21_S001_2_Outlet(Outlet_id)
on delete cascade
);


create table F21_S001_2_Customer(
Customer_id			varchar(10)	not null ,
DOB				Date			 ,
State				char(15)	not null ,
City				char(15)	not null ,
primary key (Customer_id)
);

create table F21_S001_2_Department(
Department_id			varchar(6)	not null,
Department_name			char(10)	not null,
Salary				int		not null,
Primary key (Department_id),
unique(Department_name)	
);


create table F21_S001_2_Employee(
Employee_id			varchar(8)	not null ,
Performance_rating		int		not null ,
Store_id			varchar(8)		 ,
Dept_id				varchar(6)	not null ,
primary key(Employee_id),
foreign key(Store_id) references F21_S001_2_Store(Store_id)
on delete cascade,
foreign key(Dept_id) references F21_S001_2_Department(Department_id)
on delete cascade
);


Create Table F21_S001_2_iPhone_model(
Model_name		varchar(15)	not null ,
Battery			varchar(8) 	not null ,
Processor		varchar(15)	not null ,
Camera			varchar(5)	not null ,
primary key (Model_name)
);


Create Table F21_S001_2_iPhone_initial_release(
Release_date 		DATE 	 	not null ,
Initial_value 		int 	 	not null ,
Model_name		varchar(15)	not null ,
primary key (Release_date,Initial_value),
foreign key (Model_name) references F21_S001_2_iPhone_model(Model_name)
on delete cascade
);


Create Table F21_S001_2_iPhone(
iPhone_id 		varchar(8) 	not null ,
Release_date 		DATE 	 	not null ,
Initial_value 		int 	 	not null ,
Manufacturing_price 	int 		not null ,
RAM 			varchar(4)	not null ,
Storage 		varchar(5)		 ,
Outlet_id		varchar(8)		 ,
primary key (iPhone_id),
foreign key (Release_date, Initial_value) references F21_S001_2_iPhone_initial_release (Release_date, Initial_value)
on delete cascade,
foreign key (Outlet_id) references F21_S001_2_Outlet(Outlet_id)
on delete cascade
);


create table F21_S001_2_Order_Map(
iPhone_id 		varchar(8) 	not null ,
Outlet_id		varchar(8)		 ,
primary key(iPhone_id),
foreign key (iPhone_id) references F21_S001_2_iPhone(iPhone_id),
foreign key (Outlet_id) references F21_S001_2_Outlet(Outlet_id)
);

create table F21_S001_2_Order(
Order_id		varchar(8)	not null ,
Order_date		Date	 	not null ,
Order_price		int		not null ,
Order_type		varchar(10)	not null ,
Source_of_info		varchar(15)		 ,
iPhone_id		varchar(8) 	not null ,
Customer_id		varchar(8)		 ,
primary key (Order_id),
foreign key (iPhone_id) references F21_S001_2_Order_Map(iPhone_id)
on delete cascade,
foreign key (Customer_id) references F21_S001_2_Customer(Customer_id)
on delete cascade
);


create table F21_S001_2_Order_SWC(
Order_id			varchar(8)	not null ,
Specification_with_complaint	varchar(9)		 ,
primary key(Order_id,specification_with_complaint)
);


Create table F21_S001_2_Rates(
Order_id			varchar(8)	not null ,
Customer_id			varchar(10)	not null ,
Employee_id			varchar(8)	not null ,
Rating				int			 ,
primary key(Order_id, Customer_id, Employee_id),
foreign key(Order_id)    references F21_S001_2_Order(Order_id)
on delete cascade,
foreign key(Customer_id) references F21_S001_2_Customer(Customer_id)
on delete cascade,
foreign key(Employee_id) references F21_S001_2_Employee(Employee_id)
on delete cascade
);