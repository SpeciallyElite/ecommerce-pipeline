{{ config(materialized='table') }}

with source as (
    select * from {{ref('stg_products')}}
)

select
    product_id,
    product_title,
    category,
    price as catalog_price,
    rating,
    stock,
    brand,
    loaded_at
from source