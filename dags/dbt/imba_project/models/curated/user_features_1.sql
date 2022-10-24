{{ config(materialized='table') }}

select 
    user_id,
    max(order_number) as user_orders,
    sum(days_since_prior_order) as user_period,
    round(avg(days_since_prior_order),0) as user_mean_days_since_prior
from {{ ref('orders_clean') }}
group by user_id