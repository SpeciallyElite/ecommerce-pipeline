with source as (
    select * from {{ source('ecommerce_raw', 'raw_products')}}
),

extracted as (
    select
        (products::json ->> 'id')::integer as product_id,
        products::json ->> 'title' as product_title,
        products::json ->> 'category' as category,
        (products::json ->> 'price')::numeric as price,
        (products::json ->> 'rating')::numeric as rating,
        (products::json ->> 'stock')::integer as stock,
        products::json ->> 'brand' as brand,
        loaded_at
    from source
)

select * from extracted