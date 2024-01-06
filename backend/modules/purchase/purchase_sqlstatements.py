CREATE_PURCHASE_ITEM = """ 
INSERT INTO purchase (id, supplier_id, order_date, delivery_date, raw_material_id, quantity, is_delivered, is_active, created_at, updated_at, created_by, updated_by) 
VALUES (:id, :supplier_id, :order_date, :delivery_date, :raw_material_id, :quantity, :is_delivered, :is_active, :created_at, :updated_at, :created_by, :updated_by) 
RETURNING id, supplier_id, order_date, delivery_date, raw_material_id, quantity, is_delivered, is_active, created_at, updated_at, created_by, updated_by; 
"""

GET_PURCHASE_LIST = """
    SELECT p.id, p.supplier_id, p.order_date, p.delivery_date, p.raw_material_id, p.quantity, p.is_delivered, pis_active, p.created_at, p.updated_at, 
        CAST(p.created_by AS UUID) AS created_by, 
        CAST(p.updated_by AS UUID) AS updated_by,
        us1.fullname AS created_by_name, 
        us2.fullname AS updated_by_name
    FROM purchase AS p
    LEFT JOIN users AS us1 ON us1.id = CAST(p.created_by AS UUID)
    LEFT JOIN users AS us2 ON us2.id = CAST(p.updated_by AS UUID)
"""

def purchase_list_search():
    return """ WHERE (p.order_date LIKE :search) """

def purchase_list_complements(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY p.order_date ASC;"
    elif order == "order_date" and direction == "DESC":
        sql_sentence = " ORDER BY p.order_date DESC;"
    elif order == "order_date" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY p.order_date ASC;"
    elif order == "is_delivered" and direction == "DESC":
        sql_sentence = " ORDER BY p.is_delivered DESC;"
    elif order == "is_delivered" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY p.is_delivered ASC;"

    return sql_sentence

GET_PURCHASE_BY_ID = """
    SELECT p.id, p.supplier_id, p.order_date, p.delivery_date, p.raw_material_id, p.quantity, p.is_delivered, p.is_active, p.created_at, p.updated_at, 
        CAST(p.created_by AS UUID) AS created_by, 
        CAST(p.updated_by AS UUID) AS updated_by,
        us1.fullname AS created_by_name, 
        us2.fullname AS updated_by_name
    FROM purchase AS p
    LEFT JOIN users AS us1 ON us1.id = CAST(p.created_by AS UUID)
    LEFT JOIN users AS us2 ON us2.id = CAST(p.updated_by AS UUID)
    WHERE p.id = :id; 
"""

UPDATE_PURCHASE_BY_ID = """
    UPDATE purchase
    SET supplier_id = :supplier_id,
        order_date = :order_date,
        delivery_date = :delivery_date,
        raw_material_id = :raw_material_id,
        quantity = :quantity,
        is_delivered = :is_delivered,
        is_active = :is_active,
        created_at = :created_at,
        updated_at = :updated_at,
        created_by = :created_by,
        updated_by = :updated_by
    WHERE id = :id
    RETURNING id, supplier_id, order_date, delivery_date, is_active, raw_material_id, quantity, is_delivered, created_at, updated_at, created_by, updated_by;
"""

DELETE_PURCHASE_BY_ID = """
    DELETE FROM purchase
    WHERE id = :id
    RETURNING id;
"""
