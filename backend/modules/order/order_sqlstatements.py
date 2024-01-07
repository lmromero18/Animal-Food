CREATE_ORDER_ITEM = """ 
INSERT INTO "order" (id, discount, quantity, total, is_delivered, order_date, delivery_date, is_active, product_offered_id, created_by, created_at, updated_by, updated_at) 
VALUES (:id, :discount, :quantity, :total, :is_delivered, :order_date, :delivery_date, :is_active, :product_offered_id, :created_by, :created_at, :updated_by, :updated_at) 
RETURNING id, discount, quantity, total, is_delivered, order_date, delivery_date, is_active, product_offered_id, created_by, created_at, updated_by, updated_at; 
"""

GET_ORDER_LIST = """
    SELECT o.id, o.discount, o.quantity, o.total, o.is_delivered, o.order_date, o.delivery_date, o.is_active, o.product_offered_id, o.created_at, o.updated_at, 
        CAST(o.created_by AS UUID) AS created_by, 
        CAST(o.updated_by AS UUID) AS updated_by,
        us1.fullname AS created_by_name, 
        us2.fullname AS updated_by_name
    FROM "order" AS o
    LEFT JOIN users AS us1 ON us1.id = CAST(o.created_by AS UUID)
    LEFT JOIN users AS us2 ON us2.id = CAST(o.updated_by AS UUID)
"""

def order_list_search():
    return """ WHERE (o.order_date LIKE :search) """

def order_list_complements(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY o.order_date ASC;"
    elif order == "order_date" and direction == "DESC":
        sql_sentence = " ORDER BY o.order_date DESC;"
    elif order == "order_date" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY o.order_date ASC;"
    elif order == "is_delivered" and direction == "DESC":
        sql_sentence = " ORDER BY o.is_delivered DESC;"
    elif order == "is_delivered" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY o.is_delivered ASC;"

    return sql_sentence

GET_ORDER_BY_ID = """
    SELECT o.id, o.discount, o.quantity, o.total, o.is_delivered, o.order_date, o.delivery_date, o.is_active, o.product_offered_id, o.created_at, o.updated_at, 
        CAST(o.created_by AS UUID) AS created_by, 
        CAST(o.updated_by AS UUID) AS updated_by,
        us1.fullname AS created_by_name, 
        us2.fullname AS updated_by_name
    FROM "order" AS o
    LEFT JOIN users AS us1 ON us1.id = CAST(o.created_by AS UUID)
    LEFT JOIN users AS us2 ON us2.id = CAST(o.updated_by AS UUID)
    WHERE o.id = :id; 
"""

UPDATE_ORDER_BY_ID = """
    UPDATE "order"
    SET discount = :discount,
        total = :total,
        quantity = :quantity,
        is_delivered = :is_delivered,
        order_date = :order_date,
        delivery_date = :delivery_date,
        is_active = :is_active,
        product_offered_id = :product_offered_id,
        created_at = :created_at,
        updated_at = :updated_at,
        created_by = :created_by,
        updated_by = :updated_by
    WHERE id = :id
    RETURNING id, discount, total, quantity, is_delivered, order_date, delivery_date, is_active, product_offered_id, created_at, updated_at, created_by, updated_by;
"""

DELETE_ORDER_BY_ID = """
    DELETE FROM "order"
    WHERE id = :id
    RETURNING id;
"""
