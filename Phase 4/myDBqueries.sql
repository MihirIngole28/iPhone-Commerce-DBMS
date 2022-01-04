-------------BUSINESS RULE 1------------------------
select model_name, sum(order_price) as "Selling Price", count(order_price) as "Products sold", sum(manufacturing_price) as "Manufacturing Price", sum(order_price) - sum(manufacturing_price) as "Total Profit"
from F21_S001_2_order
inner join F21_S001_2_iPhone on F21_S001_2_order.iPhone_id = F21_S001_2_iPhone.iPhone_id
inner join F21_S001_2_iPhone_initial_release on F21_S001_2_iPhone.release_date = F21_S001_2_iPhone_initial_release.release_date and F21_S001_2_iPhone.initial_value = F21_S001_2_iPhone_initial_release.initial_value
group by rollup(model_name)
order by (sum(order_price) - sum(manufacturing_price)) desc;

--------------BUSINESS RULE 2-------------------
select F21_S001_2_outlet.outlet_id, count(order_id) from F21_S001_2_outlet
inner join F21_S001_2_order_map on F21_S001_2_outlet.outlet_id = F21_S001_2_order_map.outlet_id
inner join F21_S001_2_order on F21_S001_2_order_map.iPhone_id = F21_S001_2_order.iPhone_id
group by F21_S001_2_outlet.outlet_id
having (F21_S001_2_outlet.outlet_id like 'W%')
order by count(order_id) desc
fetch first 1 rows only;

select F21_S001_2_outlet.outlet_id, count(order_id) from F21_S001_2_outlet
inner join F21_S001_2_order_map on F21_S001_2_outlet.outlet_id = F21_S001_2_order_map.outlet_id
inner join F21_S001_2_order on F21_S001_2_order_map.iPhone_id = F21_S001_2_order.iPhone_id
group by F21_S001_2_outlet.outlet_id
having (F21_S001_2_outlet.outlet_id like 'S%')
order by count(order_id) desc
fetch first 1 rows only;

-------------BUSINESS RULE 3------------------------
select count(F21_S001_2_order.order_id), model_name, city
from F21_S001_2_outlet 
inner join F21_S001_2_order_map on F21_S001_2_outlet.outlet_id = F21_S001_2_order_map.outlet_id
inner join F21_S001_2_order on F21_S001_2_order_map.iPhone_id = F21_S001_2_order.iPhone_id
inner join F21_S001_2_iPhone on F21_S001_2_order.iPhone_id = F21_S001_2_iPhone.iPhone_id
inner join F21_S001_2_iPhone_initial_release on F21_S001_2_iPhone.release_date = F21_S001_2_iPhone_initial_release.release_date and F21_S001_2_iPhone.initial_value = F21_S001_2_iPhone_initial_release.initial_value
group by cube(city,model_name)
order by count(F21_S001_2_order.order_id) desc, model_name;

---------------BUSINESS RULE 4----------------------
select count(specification_with_complaint) as "No. of complaints", specification_with_complaint, model_name
from F21_S001_2_order_swc 
inner join F21_S001_2_order on F21_S001_2_order_swc.order_id = F21_S001_2_order.order_id
inner join F21_S001_2_iPhone on F21_S001_2_order.iPhone_id = F21_S001_2_iPhone.iPhone_id
inner join F21_S001_2_iPhone_initial_release on F21_S001_2_iPhone.release_date = F21_S001_2_iPhone_initial_release.release_date and F21_S001_2_iPhone.initial_value = F21_S001_2_iPhone_initial_release.initial_value
where model_name in
(select model_name
from F21_S001_2_order
inner join F21_S001_2_iPhone on F21_S001_2_order.iPhone_id = F21_S001_2_iPhone.iPhone_id
inner join F21_S001_2_iPhone_initial_release on F21_S001_2_iPhone.release_date = F21_S001_2_iPhone_initial_release.release_date and F21_S001_2_iPhone.initial_value = F21_S001_2_iPhone_initial_release.initial_value
group by model_name
order by (count(order_price)) desc
fetch first 1 rows only)
group by specification_with_complaint,model_name
order by count(specification_with_complaint) desc;

------------------BUSINESS RULE 5------------------
select avg((order_date - DOB) / 365) as average_age from 
(select release_date,initial_value
from F21_S001_2_iPhone_initial_release where model_name in
(select model_name
from F21_S001_2_order 
inner join F21_S001_2_iPhone on F21_S001_2_order.iPhone_id = F21_S001_2_iPhone.iPhone_id
inner join F21_S001_2_iPhone_initial_release on F21_S001_2_iPhone.release_date = F21_S001_2_iPhone_initial_release.release_date and F21_S001_2_iPhone.initial_value = F21_S001_2_iPhone_initial_release.initial_value
group by model_name
order by count(order_price) desc
fetch first 1 rows only)) best_model 
inner join F21_S001_2_iPhone  on best_model.release_date = F21_S001_2_iPhone.release_date and best_model.initial_value = F21_S001_2_iPhone.initial_value
inner join F21_S001_2_order on F21_S001_2_iPhone.iPhone_id = F21_S001_2_order.iPhone_id
inner join F21_S001_2_Customer on F21_S001_2_order.customer_id = F21_S001_2_customer.customer_id;


-------------BUSINESS RULE 6------------------------
select count(source_of_info),source_of_info from F21_S001_2_order
inner join F21_S001_2_order_map on F21_S001_2_order.iPhone_id = F21_S001_2_order_map.iPhone_id
inner join F21_S001_2_outlet on F21_S001_2_order_map.outlet_id = F21_S001_2_outlet.outlet_id
where city  in
(select city
from F21_S001_2_outlet 
inner join F21_S001_2_order_map on F21_S001_2_outlet.outlet_id = F21_S001_2_order_map.outlet_id
inner join F21_S001_2_order on F21_S001_2_order_map.iPhone_id = F21_S001_2_order.iPhone_id
group by (city)
order by count(F21_S001_2_order.order_id) desc
fetch first 5 rows only)
group by source_of_info
having count(source_of_info) = 
(select max(mycount) from
(select count(source_of_info) mycount,source_of_info from F21_S001_2_order
inner join F21_S001_2_order_map on F21_S001_2_order.iPhone_id = F21_S001_2_order_map.iPhone_id
inner join F21_S001_2_outlet on F21_S001_2_order_map.outlet_id = F21_S001_2_outlet.outlet_id
where city  in
(select city
from F21_S001_2_outlet 
inner join F21_S001_2_order_map on F21_S001_2_outlet.outlet_id = F21_S001_2_order_map.outlet_id
inner join F21_S001_2_order on F21_S001_2_order_map.iPhone_id = F21_S001_2_order.iPhone_id
group by (city)
order by count(F21_S001_2_order.order_id) desc
fetch first 5 rows only)
group by source_of_info));

-----------------BUSINESS RULE 7--------------------
select department_name as "Department Name", avg(performance_rating)/5*100 as "Performance(in percent)"
from F21_S001_2_employee 
inner join F21_S001_2_department on F21_S001_2_employee.dept_id = F21_S001_2_department.department_id
group by department_name
order by avg(performance_rating) desc;


----------------BUSINESS RULE 8--------------------
select distinct user_count, model_name, source_of_info from
(select count(source_of_info) over(partition by model_name,source_of_info) as User_count, model_name, source_of_info
from F21_S001_2_order
inner join F21_S001_2_iPhone on F21_S001_2_order.iPhone_id = F21_S001_2_iPhone.iPhone_id
inner join F21_S001_2_iPhone_initial_release on F21_S001_2_iPhone.release_date = F21_S001_2_iPhone_initial_release.release_date and F21_S001_2_iPhone.initial_value = F21_S001_2_iPhone_initial_release.initial_value)
Order by model_name;


-----------------BUSINESS RULE 9-------------------
select distinct user_count, model_name,specification_with_complaint from
(select count(specification_with_complaint) over (partition by model_name,specification_with_complaint) as User_count, model_name, specification_with_complaint
from F21_S001_2_order_swc 
inner join F21_S001_2_order on F21_S001_2_order_swc.order_id = F21_S001_2_order.order_id
inner join F21_S001_2_iPhone on F21_S001_2_order.iPhone_id = F21_S001_2_iPhone.iPhone_id
inner join F21_S001_2_iPhone_initial_release on F21_S001_2_iPhone.release_date = F21_S001_2_iPhone_initial_release.release_date and F21_S001_2_iPhone.initial_value = F21_S001_2_iPhone_initial_release.initial_value)
Order by model_name;
