with source as (
    select * from {{ source('ecommerce_raw', 'raw_carts') }}
),

extracted as (
    select
        (carts::json ->> 'id')::integer as cart_id,
        (carts::json ->> 'userId')::integer as user_id,
        (p ->> 'id')::integer as product_id,
        p ->> 'title' as title,
        (p ->> 'price')::numeric as price,
        (p ->> 'quantity')::integer as quantity,
        (p ->> 'total')::numeric as total,
        (p ->> 'discountPercentage')::numeric as discountPercentage,
        loaded_at
    from source
    cross join lateral json_array_elements((carts::json) -> 'products') as p
),

ranked_carts as (
    select
        cart_id,
        user_id,
        product_id,
        title,
        price,
        quantity,
        total,
        discountPercentage,
        loaded_at,
        row_number() over (
            partition by cart_id, product_id
            order by loaded_at desc
        ) as rn
    from extracted
)

select
    cart_id,
    user_id,
    product_id,
    title,
    price,
    quantity,
    total,
    discountPercentage,
    loaded_at
from ranked_carts
where rn = 1
