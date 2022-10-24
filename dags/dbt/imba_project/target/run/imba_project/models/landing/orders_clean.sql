

      create or replace transient table IMBA.dev_landing.orders_clean  as
      (

select 
    *
    
from imba.raw.orders
      );
    