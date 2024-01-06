CREATE_PRICE_ITEM = """
INSERT INTO price (id, price, is_active, created_at, updated_at, created_by, updated_by)
VALUES (:id, :price, :is_active, :created_at, :updated_at, :created_by, :updated_by)
RETURNING id, price, is_active, created_at, updated_at, created_by, updated_by
"""

GET_PRICE_LIST = """
SELECT p.id, p.price, p.is_active, p.created_at, p.updated_at,
    CAST(p.created_by AS UUID) AS created_by,
    CAST(p.updated_by AS UUID) AS updated_by,
    us1.fullname AS created_by_name,
    us2.fullname AS updated_by_name
FROM price AS p
LEFT JOIN users AS us1 ON us1.id = CAST(p.created_by AS UUID)
LEFT JOIN users AS us2 ON us2.id = CAST(p.updated_by AS UUID)
"""

def price_list_search():
    return """ WHERE (p.price::text LIKE :search) """

def price_list_complements(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY p.price ASC;"
    elif order == "price" and direction == "DESC":
        sql_sentence = " ORDER BY p.price DESC;"
    elif order == "price" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY p.price ASC;"
    elif order == "status" and direction == "DESC":
        sql_sentence = " ORDER BY p.is_active DESC;"
    elif order == "status" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY p.is_active ASC;"

    return sql_sentence


    return sql_sentence

GET_PRICE_BY_ID = """
SELECT p.id, p.price, p.is_active, p.created_at, p.updated_at,
    CAST(p.created_by AS UUID) AS created_by,
    CAST(p.updated_by AS UUID) AS updated_by,
    us1.fullname AS created_by_name,
    us2.fullname AS updated_by_name
FROM price AS p
LEFT JOIN users AS us1 ON us1.id = CAST(p.created_by AS UUID)
LEFT JOIN users AS us2 ON us2.id = CAST(p.updated_by AS UUID)
WHERE p.id = :id
"""

UPDATE_PRICE_BY_ID = """
UPDATE price
SET price = :price,
    is_active = :is_active,
    created_at = :created_at,
    updated_at = :updated_at,
    created_by = :created_by,
    updated_by = :updated_by
WHERE id = :id
RETURNING id, price, is_active, created_at, updated_at, created_by, updated_by;
"""

DELETE_PRICE_BY_ID = """
DELETE FROM price
WHERE id = :id
RETURNING id
"""