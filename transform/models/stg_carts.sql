with source as (
    select * from {{ source('ecommerce_raw', 'raw_carts') }}
),

extracted as (
    select
        (carts::json ->> 'id')::integer as cart_id,
        (carts::json ->> 'userId')::integer as user_id,
        (p ->> 'id')::integer as id,
        p ->> 'title' as title,
        (p ->> 'price')::numeric as price,
        (p ->> 'quantity')::integer as quantity,
        (p ->> 'total')::numeric as total
    from source
    cross join lateral json_array_elements((carts::json) -> 'products') as p
)

select * from extracted
