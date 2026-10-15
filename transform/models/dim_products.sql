{{ config(materialized='table') }}

with source as(
    select * from {{ref('int_cart_items')}}
)

select
    cart_id,
    user_id,
    product_id,
    quantity,
    cart_item_price,
    total,
    discountPercentage,
    final_discounted_total,
    product_title,
    catalog_price,
    category,
    loaded_at
from source