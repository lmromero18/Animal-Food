CREATE_PRODUCT_ITEM = """ 
INSERT INTO product (id, name, description, quantity, price, is_active, created_at, updated_at, created_by, updated_by, warehouse_id) 
VALUES (:id, :name, :description, :quantity, :price, :is_active, :created_at, :updated_at, :created_by, :updated_by, :warehouse_id) 
RETURNING id, name, description, quantity, price, is_active, created_at, updated_at, created_by, updated_by, warehouse_id; 
"""

GET_PRODUCT_LIST = """
    SELECT p.id, p.name, p.description, p.quantity, p.price, p.is_active, p.created_at, p.updated_at, 
        CAST(p.created_by AS UUID) AS created_by, 
        CAST(p.updated_by AS UUID) AS updated_by,
        us1.fullname AS created_by_name, 
        us2.fullname AS updated_by_name,
        w.id AS warehouse_id,
        w.name AS warehouse_name
    FROM product AS p
    LEFT JOIN users AS us1 ON us1.id = CAST(p.created_by AS UUID)
    LEFT JOIN users AS us2 ON us2.id = CAST(p.updated_by AS UUID)
    LEFT JOIN warehouse AS w ON w.id = p.warehouse_id
"""

def product_list_search():
    return """ WHERE (p.name LIKE :search) """

def product_list_complements(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY p.name ASC;"
    elif order == "name" and direction == "DESC":
        sql_sentence = " ORDER BY p.name DESC;"
    elif order == "name" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY p.name ASC;"
    elif order == "status" and direction == "DESC":
        sql_sentence = " ORDER BY p.is_active DESC;"
    elif order == "status" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY p.is_active ASC;"

    return sql_sentence

GET_PRODUCT_BY_ID = """
    SELECT p.id, p.name, p.description, p.quantity, p.price, p.is_active, p.created_at, p.updated_at, 
        CAST(p.created_by AS UUID) AS created_by, 
        CAST(p.updated_by AS UUID) AS updated_by,
        us1.fullname AS created_by_name, 
        us2.fullname AS updated_by_name,
        w.id AS warehouse_id,
        w.name AS warehouse_name
    FROM product AS p
    LEFT JOIN users AS us1 ON us1.id = CAST(p.created_by AS UUID)
    LEFT JOIN users AS us2 ON us2.id = CAST(p.updated_by AS UUID)
    LEFT JOIN warehouse AS w ON w.id = p.warehouse_id
    WHERE p.id = :id; 
"""

UPDATE_PRODUCT_BY_ID = """
    UPDATE product
    SET name = :name,
        description = :description,
        quantity = :quantity,
        price = :price,
        is_active = :is_active,
        created_at = :created_at,
        updated_at = :updated_at,
        created_by = :created_by,
        updated_by = :updated_by,
        warehouse_id = :warehouse_id
    WHERE id = :id
    RETURNING id, name, description, quantity, price, is_active, created_at, updated_at, created_by, updated_by, warehouse_id;
"""

DELETE_PRODUCT_BY_ID = """
    DELETE FROM product
    WHERE id = :id
    RETURNING id;
"""