with products as (
    select * from {{ ref('stg_products') }}
),

carts as (
    select * from {{ ref('stg_carts') }}
)

select
    carts.cart_id,
    carts.user_id,
    carts.product_id,
    carts.quantity,
    carts.price as cart_item_price,
    carts.total,
    carts.discountPercentage,
    ROUND((carts.total - (carts.total * (carts.discountPercentage/100))), 2) AS final_discounted_total,
    carts.loaded_at,
    products.product_title,
    products.price as catalog_price,
    products.category
from carts
left join products
    on carts.product_id = products.product_id