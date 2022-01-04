import cx_Oracle
import pandas as pd

try:
    connection = cx_Oracle.connect(user="<username>", password="<password>",
                       dsn="acaddbprod-2.uta.edu:1523/pcse1p.data.uta.edu",
                       encoding="UTF-8")
    cursor = connection.cursor()
    print("oracle connection successful")

except cx_Oracle.DatabaseError as e:
    print("Problem with connection Oracle: ",e)

def create_tables():

    sql_create_F21_S001_2_Outlet = """
    create table F21_S001_2_Outlet(
    Outlet_id		varchar(8)	not null ,
    City			char(15)	not null ,
    State			char(15)	not null ,
    primary key (Outlet_id)
    )
    """

    sql_create_F21_S001_2_Warehouse = """
    create table F21_S001_2_Warehouse(
    Warehouse_id		varchar(8)	not null ,
    primary key(Warehouse_id),
    foreign key(Warehouse_id) references F21_S001_2_Outlet(Outlet_id)
    on delete cascade
    )
    """


    sql_create_F21_S001_2_Store = """
    create table F21_S001_2_Store(
    Store_id		varchar(8)	not null ,
    primary key(Store_id),
    foreign key(Store_id) references F21_S001_2_Outlet(Outlet_id)
    on delete cascade
    )
    """

    sql_create_F21_S001_2_Customer = """
    create table F21_S001_2_Customer(
    Customer_id			varchar(10)	not null ,
    DOB				Date			 ,
    State				char(15)	not null ,
    City				char(15)	not null ,
    primary key (Customer_id)
    )
    """

    sql_create_F21_S001_2_Department = """
    create table F21_S001_2_Department(
    Department_id			varchar(6)	not null,
    Department_name			char(10)	not null,
    Salary				int		not null,
    Primary key (Department_id),
    unique(Department_name)	
    )
    """

    sql_create_F21_S001_2_Employee = """
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
    )
    """

    sql_create_F21_S001_2_iPhone_model = """
    Create Table F21_S001_2_iPhone_model(
    Model_name		varchar(15)	not null ,
    Battery			varchar(8) 	not null ,
    Processor		varchar(15)	not null ,
    Camera			varchar(5)	not null ,
    primary key (Model_name)
    )
    """

    sql_create_F21_S001_2_iPhone_initial_release = """
    Create Table F21_S001_2_iPhone_initial_release(
    Release_date 		DATE 	 	not null ,
    Initial_value 		int 	 	not null ,
    Model_name		varchar(15)	not null ,
    primary key (Release_date,Initial_value),
    foreign key (Model_name) references F21_S001_2_iPhone_model(Model_name)
    on delete cascade
    )
    """

    sql_create_F21_S001_2_iPhone = """
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
    )
    """

    sql_create_F21_S001_2_Order_Map = """
    create table F21_S001_2_Order_Map(
    iPhone_id 		varchar(8) 	not null ,
    Outlet_id		varchar(8)		 ,
    primary key(iPhone_id),
    foreign key (iPhone_id) references F21_S001_2_iPhone(iPhone_id),
    foreign key (Outlet_id) references F21_S001_2_Outlet(Outlet_id)
    )
    """


    sql_create_F21_S001_2_Order = """
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
    )
    """

    sql_create_F21_S001_2_Order_SWC = """
    create table F21_S001_2_Order_SWC(
    Order_id			varchar(8)	not null ,
    Specification_with_complaint	varchar(9)		 ,
    primary key(Order_id,specification_with_complaint)
    )
    """

    sql_create_F21_S001_2_Rates = """
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
    )
    """

    create_tables = [sql_create_F21_S001_2_Outlet,sql_create_F21_S001_2_Warehouse,sql_create_F21_S001_2_Store,sql_create_F21_S001_2_Customer,sql_create_F21_S001_2_Department,sql_create_F21_S001_2_Employee,sql_create_F21_S001_2_iPhone_model,sql_create_F21_S001_2_iPhone_initial_release,sql_create_F21_S001_2_iPhone,sql_create_F21_S001_2_Order_Map,sql_create_F21_S001_2_Order,sql_create_F21_S001_2_Order_SWC,sql_create_F21_S001_2_Rates]
    
    for table in create_tables:
        try:
            cursor.execute(table)
            print('Table created.')
        except cx_Oracle.DatabaseError as e:
            print("Table creation error: ",e)
            
            
def drop_tables():
    
    sql_drop_F21_S001_2_Rates = "drop table F21_S001_2_Rates"
    sql_drop_F21_S001_2_Order_SWC = "drop table F21_S001_2_Order_SWC"
    sql_drop_F21_S001_2_Order = "drop table F21_S001_2_Order"
    sql_drop_F21_S001_2_Order_Map = "drop table F21_S001_2_Order_Map"
    sql_drop_F21_S001_2_iPhone = "drop table F21_S001_2_iPhone"
    sql_drop_F21_S001_2_iPhone_initial_release = "drop table F21_S001_2_iPhone_initial_release"
    sql_drop_F21_S001_2_iPhone_model = "drop table F21_S001_2_iPhone_model"
    sql_drop_F21_S001_2_Employee = "drop table F21_S001_2_Employee"
    sql_drop_F21_S001_2_Department = "drop table F21_S001_2_Department"
    sql_drop_F21_S001_2_Customer = "drop table F21_S001_2_Customer"
    sql_drop_F21_S001_2_Store = "drop table F21_S001_2_Store"
    sql_drop_F21_S001_2_Warehouse = "drop table F21_S001_2_Warehouse"
    sql_drop_F21_S001_2_Outlet = "drop table F21_S001_2_Outlet"


    drop_tables = [sql_drop_F21_S001_2_Rates,sql_drop_F21_S001_2_Order_SWC,sql_drop_F21_S001_2_Order,sql_drop_F21_S001_2_Order_Map,sql_drop_F21_S001_2_iPhone,sql_drop_F21_S001_2_iPhone_initial_release,sql_drop_F21_S001_2_iPhone_model,sql_drop_F21_S001_2_Employee,sql_drop_F21_S001_2_Department,sql_drop_F21_S001_2_Customer,sql_drop_F21_S001_2_Store,sql_drop_F21_S001_2_Warehouse,sql_drop_F21_S001_2_Outlet]
    
    for table in drop_tables:
        try:
            cursor.execute(table)
            print('Table dropped.')
        except cx_Oracle.DatabaseError as e:
            print("Table deletion error: ",e)


def insert_records():
    insert_records = open('insert.txt', 'r')
    records = insert_records.readlines()
    cursor.execute("Alter session set NLS_DATE_FORMAT = 'YYYY-MM-DD'")
    for record in records:
        try:
            cursor.execute(record)
            print('Record inserted successfully.')
        except cx_Oracle.DatabaseError as e:
            print("Record insertion error: ",e)
    insert_records.close()
    
    
    
def show_iPhone_model():
    contents_of_F21_S001_2_iPhone_model = "Select * from F21_S001_2_iPhone_model"
    
    try:
        im = cursor.execute(contents_of_F21_S001_2_iPhone_model)
    except cx_Oracle.DatabaseError as e:
        print("Error in table display: ",e)

    modelList = []
    for elem in im:
        myList = []
        for i in range(len(elem)):
            myList.append(elem[i])
        modelList.append(myList)

    df_iPhone_model = pd.DataFrame (modelList,columns = ['iPhone model','Battery','Processor', 'Camera'])
    df_iPhone_model.index += 1
    print(df_iPhone_model)
    
def show_Order():
    contents_of_F21_S001_2_Order = "Select * from F21_S001_2_Order"
    
    try:
        Or = cursor.execute(contents_of_F21_S001_2_Order)
    except cx_Oracle.DatabaseError as e:
        print("Error in table display: ",e)

    OrderList = []
    for elem in Or:
        myList = []
        for i in range(len(elem)):
            myList.append(elem[i])
        OrderList.append(myList)

    df_Order = pd.DataFrame (OrderList,columns = ['Order ID','Order Date','Order Total', 'Order Type','Source of Info', 'iPhone ID', 'Customer ID'])
    df_Order.index += 1
    print(df_Order)
    
def show_outlet():
    contents_of_F21_S001_2_Outlet = "Select * from F21_S001_2_Outlet"
    
    try:
        Ou = cursor.execute(contents_of_F21_S001_2_Outlet)
    except cx_Oracle.DatabaseError as e:
        print("Error in table display: ",e)

    outletList = []
    for elem in Ou:
        myList = []
        for i in range(len(elem)):
            myList.append(elem[i])
        outletList.append(myList)

    df_Outlet = pd.DataFrame (outletList,columns = ['Outlet ID','City','State'])
    df_Outlet.index += 1
    print(df_Outlet)
    
    
def insert_rec_outlet():
    
    while True:
        outlet_id = input('Enter the outlet id of the outlet: ')
        if outlet_id[0] in ['W','S'] and len(outlet_id) == 8:
            break
        else:
            print('An outlet ID must start with a \'W\' or \'S\', and total length must be 8 characters')
            
    
    while True:
        City = input('Enter the City of the outlet: ')
        if len(City) <= 15:
            break
        else:
            print('Length of string too long. Please try again')
            
    
    while True:
        State = input('Enter the State of the outlet: ')
        if len(State) <= 15:
            break
        else:
            print('Length of string too long. Please try again')
            
            
    insert_record_outlet = "insert into F21_S001_2_Outlet (Outlet_id,City,State) values ('"+outlet_id+"', '"+City+"','"+State+"')"
    
    try:
        cursor.execute(insert_record_outlet)
        print('Record inserted successfully.')
    except cx_Oracle.DatabaseError as e:
        print("Record insertion error: ",e)
    
    
def update_order_rec():
    while True:
        order_id = input('Please enter the Order ID: ')

        try:
            cnt = cursor.execute("Select count(*) from F21_S001_2_Order where Order_id = '"+order_id+"'")
            for c in cnt:
                tempc = c[0]
            if tempc == 0:
                print("Order ID not found. Please try again.")
                continue
            else:
                pass
        except:
            pass

        case = input('''Please choose one of the following: 
        1). Update the order price
        2). Update the order type
        3). Update the source through which the customer came to know about the product
        ''')
        if case == '':
            print('Invalid input. Please try again.')
            continue
        else:
            pass

        if int(case) == 1:
            order_price = input("Please enter the order price: ")
            if order_price == '':
                print('Invalid input. Please try again.')
                continue
            else:
                pass

            if int(order_price) >= 700 and int(order_price) <= 1299:
                try:
                    update_record_order_price = "update F21_S001_2_Order set Order_price = "+order_price+" where Order_id = '"+order_id+"'"
                    cursor.execute(update_record_order_price)
                    print('Updated successfully.')
                    try:
                        opTemp = cursor.execute("Select * from F21_S001_2_Order where order_id = '"+order_id+"'")
                    except cx_Oracle.DatabaseError as e:
                        print("Error while displaying the record: ",e)
                    opList = []
                    for elem in opTemp:
                        myList = []
                        for i in range(len(elem)):
                            myList.append(elem[i])
                        opList.append(myList)
                    df_Order_price = pd.DataFrame (opList,columns = ['Order ID','Order Date','Order Total', 'Order Type','Source of Info', 'iPhone ID', 'Customer ID'])
                    print(df_Order_price)
                    break
                except cx_Oracle.DatabaseError as e:
                    print("Error while updating: ",e)
                    print("Please try again.")
            else:
                print("Invalid order price. Please try again.")

        elif int(case) == 2:
            order_type = input("Please enter the order type (Online or In-Person): ")
            if order_type == '':
                print('Invalid input. Please try again.')
                continue
            else:
                pass            
            if order_type in ["Online","In-Person"]:
                try:
                    update_record_order_type = "update F21_S001_2_Order set Order_type = '"+order_type+"' where Order_id = '"+order_id+"'"
                    cursor.execute(update_record_order_type)
                    print('Updated successfully.')
                    try:
                        otTemp = cursor.execute("Select * from F21_S001_2_Order where order_id = '"+order_id+"'")
                    except cx_Oracle.DatabaseError as e:
                        print("Error while displaying the record: ",e)
                    opList = []
                    for elem in otTemp:
                        myList = []
                        for i in range(len(elem)):
                            myList.append(elem[i])
                        opList.append(myList)
                    df_Order_price = pd.DataFrame (opList,columns = ['Order ID','Order Date','Order Total', 'Order Type','Source of Info', 'iPhone ID', 'Customer ID'])
                    print(df_Order_price)
                    break
                except cx_Oracle.DatabaseError as e:
                    print("Error while updating: ",e)
                    print("Please try again.")
            else:
                print("Invalid order type. Please try again.")

        elif int(case) == 3:
            source_of_info = input("Please enter the source through which the customer came to know about the product")
            if source_of_info == '':
                print('Invalid input. Please try again.')
                continue
            else:
                pass 
            if source_of_info in ["Commercial","Social Media","Newspaper","Promotion email"]:
                try:    
                    update_record_order_soi = "update F21_S001_2_Order set Source_of_info = '"+source_of_info+"' where Order_id = '"+order_id+"'"
                    cursor.execute(update_record_order_soi)
                    print('Updated successfully.')
                    try:
                        soiTemp = cursor.execute("Select * from F21_S001_2_Order where order_id = '"+order_id+"'")
                    except cx_Oracle.DatabaseError as e:
                        print("Error while displaying the record: ",e)
                    opList = []
                    for elem in soiTemp:
                        myList = []
                        for i in range(len(elem)):
                            myList.append(elem[i])
                        opList.append(myList)
                    df_Order_price = pd.DataFrame (opList,columns = ['Order ID','Order Date','Order Total', 'Order Type','Source of Info', 'iPhone ID', 'Customer ID'])
                    print(df_Order_price)
                    break
                except cx_Oracle.DatabaseError as e:
                    print("Error while updating: ",e)
            else:
                print("Invalid source of info. Please try again.")
        else:
            print('Invalid input. Please try again')
            
            
            
def show_business_rule_1():
    
    model_list = ['iPhone X','iPhone 11','iPhone 11 Pro','iPhone 12','iPhone 12 Pro','iPhone 13','iPhone 13 Pro']
    while True:
        model_name = input("Enter the model name: ")
        if model_name in model_list:
            break
        else:
            print('Invalid model name. Please try again.')
   

    business_rule_1 = '''
select model_name, sum(order_price) as "Selling Price", count(order_price) as "Products sold", sum(manufacturing_price) as "Manufacturing Price", sum(order_price) - sum(manufacturing_price) as "Total Profit"
from F21_S001_2_order
inner join F21_S001_2_iPhone on F21_S001_2_order.iPhone_id = F21_S001_2_iPhone.iPhone_id
inner join F21_S001_2_iPhone_initial_release on F21_S001_2_iPhone.release_date = F21_S001_2_iPhone_initial_release.release_date and F21_S001_2_iPhone.initial_value = F21_S001_2_iPhone_initial_release.initial_value
where model_name = '''"'"+model_name+"'"''' or model_name = '''"'"+model_name+" Pro'"'''
group by rollup(model_name)
order by (sum(order_price) - sum(manufacturing_price)) desc
'''
    business_rule_1_X = '''
select model_name, sum(order_price) as "Selling Price", count(order_price) as "Products sold", sum(manufacturing_price) as "Manufacturing Price", sum(order_price) - sum(manufacturing_price) as "Total Profit"
from F21_S001_2_order
inner join F21_S001_2_iPhone on F21_S001_2_order.iPhone_id = F21_S001_2_iPhone.iPhone_id
inner join F21_S001_2_iPhone_initial_release on F21_S001_2_iPhone.release_date = F21_S001_2_iPhone_initial_release.release_date and F21_S001_2_iPhone.initial_value = F21_S001_2_iPhone_initial_release.initial_value
where model_name = '''"'"+model_name+"'"'''
group by rollup(model_name)
order by (sum(order_price) - sum(manufacturing_price)) desc
'''
    
    if model_name == 'iPhone X':
        try:
            br1 = cursor.execute(business_rule_1_X)
        except cx_Oracle.DatabaseError as e:
            print("Business rule 1 error: ",e)

        br1List = []
        for elem in br1:
            myList = []
            for i in range(len(elem)):
                myList.append(elem[i])
            br1List.append(myList)

        df_br1 = pd.DataFrame (br1List,columns = ['Model Name','Selling Price','Products sold','Manufacturing Price','Total Profit'],index = ['Total',1])
        print(df_br1)

    else:
        try:
            br1 = cursor.execute(business_rule_1)
        except cx_Oracle.DatabaseError as e:
            print("Business rule 1 error: ",e)

        br1List = []
        for elem in br1:
            myList = []
            for i in range(len(elem)):
                myList.append(elem[i])
            br1List.append(myList)

        df_br1 = pd.DataFrame (br1List,columns = ['Model Name','Selling Price','Products sold','Manufacturing Price','Total Profit'],index = ['Total',1,2])

        print(df_br1)
        
        
        
def show_business_rule_2():
    
    while True:
        outlet_initial = input('''
Enter the outlet type initial:
W for Warehouses
S for Stores

''')
        if outlet_initial in ['W','S']:
            break
        else:
            print('Invalid model name. Please try again.')
   

    business_rule_2 = '''
select F21_S001_2_outlet.outlet_id, count(order_id) from F21_S001_2_outlet
inner join F21_S001_2_order_map on F21_S001_2_outlet.outlet_id = F21_S001_2_order_map.outlet_id
inner join F21_S001_2_order on F21_S001_2_order_map.iPhone_id = F21_S001_2_order.iPhone_id
group by F21_S001_2_outlet.outlet_id
having (F21_S001_2_outlet.outlet_id like '''"'"+outlet_initial+'''%')
order by count(order_id) desc
fetch first 1 rows only
'''

    try:
        br2 = cursor.execute(business_rule_2)
    except cx_Oracle.DatabaseError as e:
        print("Business rule 2 error: ",e)

    br2List = []
    for elem in br2:
        myList = []
        for i in range(len(elem)):
            myList.append(elem[i])
        br2List.append(myList)

    df_br2 = pd.DataFrame (br2List,columns = ['Outlet ID','Total iPhones sold'],index = [1])

    print(df_br2)
    
    
    
def show_business_rule_3():
    
    model_list = ['iPhone X','iPhone 11','iPhone 11 Pro','iPhone 12','iPhone 12 Pro','iPhone 13','iPhone 13 Pro']
    while True:
        model_name_1 = input('Enter the name of 1st model: ')
        model_name_2 = input('Enter the name of 2nd model: ')
        if model_name_1 in model_list and model_name_2 in model_list and model_name_1 != model_name_2:
            break
        else:
            print('Invalid model name. Please try again.')
   
    business_rule_3 = '''
select count(F21_S001_2_order.order_id), model_name, city
from F21_S001_2_outlet 
inner join F21_S001_2_order_map on F21_S001_2_outlet.outlet_id = F21_S001_2_order_map.outlet_id
inner join F21_S001_2_order on F21_S001_2_order_map.iPhone_id = F21_S001_2_order.iPhone_id
inner join F21_S001_2_iPhone on F21_S001_2_order.iPhone_id = F21_S001_2_iPhone.iPhone_id
inner join F21_S001_2_iPhone_initial_release on F21_S001_2_iPhone.release_date = F21_S001_2_iPhone_initial_release.release_date and F21_S001_2_iPhone.initial_value = F21_S001_2_iPhone_initial_release.initial_value
where model_name in ('''"'"+model_name_1+"','"+model_name_2+"'"''')
group by cube(city,model_name)
order by city
'''


    try:
        br3 = cursor.execute(business_rule_3)
    except cx_Oracle.DatabaseError as e:
        print("Business rule 3 error: ",e)

    br3List = []
    for elem in br3:
        myList = []
        for i in range(len(elem)):
            myList.append(elem[i])
        br3List.append(myList)

    df_br3 = pd.DataFrame (br3List,columns = ['iPhones sold','iPhone model','City'],index = None)

    print(df_br3)
    
    
def close_connection():
    if cursor:
        cursor.close()
    if connection:
        connection.close()
        
        
        
while True:
    menu = input('''
    x---------------------iPhone Commerce DBMS----------------------X


    Welcome!

    Please select one of the following:
    1). Refresh database. (May take a while)
    2). Display relations.
    3). Modify relations.
    4). Generate reports.
    5). Finish up.
    ''')
    if menu in ['1','2','3','4','5']:
        pass
    else:
        print('Invalid input. Please try again.')
        continue
        
    if int(menu) == 1:
        
        drop_tables()
        create_tables()
        insert_records()
    elif int(menu) == 2:

        while True:
            menu2 = input('''


            1). iPhone model table.
            2). Order table.
            3). Outlet table.
            4). Go back to the previous menu.
            ''')
            if menu2 in ['1','2','3','4']:
                pass
            else:
                print('Invalid input. Please try again.')
                continue
            
            if int(menu2) == 1:
                show_iPhone_model()
            elif int(menu2) == 2:
                show_Order()
            elif int(menu2) == 3:
                show_outlet()
            elif int(menu2) == 4:
                break
            else:
                print('Invalid input. Please try again.')
    elif int(menu) == 3:
        while True:
            menu3 = input('''


            1). Insert record in Outlet table.
            2). Modify an Order table record.
            3). Go back to the previous menu.
            ''')
            if menu3 in ['1','2','3']:
                pass
            else:
                print('Invalid input. Please try again.')
                continue

            if int(menu3) == 1:
                insert_rec_outlet()
            elif int(menu3) == 2:
                update_order_rec()
            elif int(menu3) == 3:
                break
            else:
                print('Invalid input. Please try again.')

    elif int(menu) == 4:
        while True:
            menu4 = input('''


            1). Get information regarding quantity of each model sold and expenses report of a model and it's counterpart.
            2). Get information regarding best performing Store or Warehouse.
            3). Compare 2 models and it's sales across all cities.
            4). Go back to the previous menu.
            ''')

            if menu4 in ['1','2','3','4']:
                pass
            else:
                print('Invalid input. Please try again.')
                continue
                
            if int(menu4) == 1:
                show_business_rule_1()
            elif int(menu4) == 2:
                show_business_rule_2()
            elif int(menu4) == 3:
                show_business_rule_3()
            elif int(menu4) == 4:
                break
            else:
                print('Invalid input. Please try again.')

    elif int(menu) == 5:
        close_connection()
        break

    else:
        print('Invalid input. Please try again.')