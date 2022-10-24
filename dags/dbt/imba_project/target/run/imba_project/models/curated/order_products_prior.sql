

      create or replace transient table IMBA.dev_curated.order_products_prior  as
      (

select 
    a.*, 
    b.product_id, 
    b.add_to_cart_order,
    b.reordered
from IMBA.dev_landing.orders_clean a 
join IMBA.dev_landing.orders_products_clean b
on a.order_id = b.order_id
where a.eval_set = 'prior'
      );
    