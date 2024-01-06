CREATE_SUPPLIER_ITEM = """
INSERT INTO supplier (id, name, address, is_active, created_at, updated_at, created_by, updated_by)
VALUES (:id, :name, :address, :is_active, :created_at, :updated_at, :created_by, :updated_by)
RETURNING id, name, address, is_active, created_at, updated_at, created_by, updated_by
"""

GET_SUPPLIER_LIST = """
SELECT s.id, s.name, s.address, s.is_active, s.created_at, s.updated_at,
    CAST(s.created_by AS UUID) AS created_by,
    CAST(s.updated_by AS UUID) AS updated_by,
    us1.fullname AS created_by_name,
    us2.fullname AS updated_by_name
FROM supplier AS s
LEFT JOIN users AS us1 ON us1.id = CAST(s.created_by AS UUID)
LEFT JOIN users AS us2 ON us2.id = CAST(s.updated_by AS UUID)
"""

def supplier_list_search():
    return """ WHERE (s.name LIKE :search) """

def supplier_list_complements(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY s.name ASC;"
    elif order == "name" and direction == "DESC":
        sql_sentence = " ORDER BY s.name DESC;"
    elif order == "name" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY s.name ASC;"
    elif order == "status" and direction == "DESC":
        sql_sentence = " ORDER BY s.is_active DESC;"
    elif order == "status" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY s.is_active ASC;"

    return sql_sentence

GET_SUPPLIER_BY_ID = """
SELECT s.id, s.name, s.address, s.is_active, s.created_at, s.updated_at,
    CAST(s.created_by AS UUID) AS created_by,
    CAST(s.updated_by AS UUID) AS updated_by,
    us1.fullname AS created_by_name,
    us2.fullname AS updated_by_name
FROM supplier AS s
LEFT JOIN users AS us1 ON us1.id = CAST(s.created_by AS UUID)
LEFT JOIN users AS us2 ON us2.id = CAST(s.updated_by AS UUID)
WHERE s.id = :id
"""

UPDATE_SUPPLIER_BY_ID = """
UPDATE supplier
SET name = :name,
    address = :address,
    is_active = :is_active,
    created_at = :created_at,
    updated_at = :updated_at,
    created_by = :created_by,
    updated_by = :updated_by
WHERE id = :id
RETURNING id, name, address, is_active, created_at, updated_at, created_by, updated_by;
"""

DELETE_SUPPLIER_BY_ID = """
DELETE FROM supplier
WHERE id = :id
RETURNING id
"""
