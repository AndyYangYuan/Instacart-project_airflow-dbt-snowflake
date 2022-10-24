{{ config(materialized='table') }}

select 
    *

from imba.raw.orders_products