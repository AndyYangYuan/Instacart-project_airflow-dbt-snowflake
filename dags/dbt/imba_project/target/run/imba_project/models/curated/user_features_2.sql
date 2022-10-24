

      create or replace transient table IMBA.dev_curated.user_features_2  as
      (

select 
    user_id,
    count(product_id) as user_total_products,
    count(distinct product_id) as user_distinct_products,
    round(cast(sum(reordered) as double)/cast(sum(case when order_number>1 then 1 else 0 end) as double),2) as user_reorder_ratio
from IMBA.dev_curated.order_products_prior
group by user_id
      );
    