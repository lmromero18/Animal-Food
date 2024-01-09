CREATE_RAW_MATERIAL_ITEM = """
INSERT INTO rawmaterial (id, code, name, available_quantity, is_active, created_at, updated_at, created_by, updated_by, warehouse_id)
VALUES (:id, :code, :name, :available_quantity, :is_active, :created_at, :updated_at, :created_by, :updated_by, :warehouse_id)
RETURNING id, code, name, available_quantity, is_active, created_at, updated_at, created_by, updated_by, warehouse_id
"""

GET_RAW_MATERIAL_LIST = """
SELECT rm.id, rm.code, rm.name, rm.available_quantity, rm.is_active, rm.created_at, rm.updated_at,
    CAST(rm.created_by AS UUID) AS created_by,
    CAST(rm.updated_by AS UUID) AS updated_by,
    us1.fullname AS created_by_name,
    us2.fullname AS updated_by_name,
    w.id AS warehouse_id,
    w.name AS warehouse_name
FROM rawmaterial AS rm
LEFT JOIN users AS us1 ON us1.id = CAST(rm.created_by AS UUID)
LEFT JOIN users AS us2 ON us2.id = CAST(rm.updated_by AS UUID)
LEFT JOIN warehouse AS w ON w.id = rm.warehouse_id
"""

def raw_material_list_search():
    return """ WHERE (rm.name LIKE :search) """

def raw_material_list_complements(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY rm.name ASC;"
    elif order == "name" and direction == "DESC":
        sql_sentence = " ORDER BY rm.name DESC;"
    elif order == "name" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY rm.name ASC;"
    elif order == "status" and direction == "DESC":
        sql_sentence = " ORDER BY rm.is_active DESC;"
    elif order == "status" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY rm.is_active ASC;"

    return sql_sentence

GET_RAW_MATERIAL_BY_ID = """
SELECT rm.id, rm.code, rm.name, rm.available_quantity, rm.is_active, rm.created_at, rm.updated_at,
    CAST(rm.created_by AS UUID) AS created_by,
    CAST(rm.updated_by AS UUID) AS updated_by,
    us1.fullname AS created_by_name,
    us2.fullname AS updated_by_name,
    w.id AS warehouse_id,
    w.name AS warehouse_name
FROM rawmaterial AS rm
LEFT JOIN users AS us1 ON us1.id = CAST(rm.created_by AS UUID)
LEFT JOIN users AS us2 ON us2.id = CAST(rm.updated_by AS UUID)
LEFT JOIN warehouse AS w ON w.id = rm.warehouse_id
WHERE rm.id = :id
"""

UPDATE_RAW_MATERIAL_BY_ID = """
UPDATE rawmaterial
SET code = :code,
    name = :name,
    available_quantity = :available_quantity,
    is_active = :is_active,
    created_at = :created_at,
    updated_at = :updated_at,
    created_by = :created_by,
    updated_by = :updated_by,
    warehouse_id = :warehouse_id
WHERE id = :id
RETURNING id, code, name, available_quantity, is_active, created_at, updated_at, created_by, updated_by, warehouse_id;
"""

DELETE_RAW_MATERIAL_BY_ID = """
DELETE FROM rawmaterial
WHERE id = :id
RETURNING id
"""

GET_RAW_MATERIAL_BY_CODE = """
SELECT rm.id, rm.code, rm.name, rm.available_quantity, rm.is_active, rm.created_at, rm.updated_at,
    CAST(rm.created_by AS UUID) AS created_by,
    CAST(rm.updated_by AS UUID) AS updated_by,
    us1.fullname AS created_by_name,
    us2.fullname AS updated_by_name,
    w.id AS warehouse_id,
    w.name AS warehouse_name
FROM rawmaterial AS rm
LEFT JOIN users AS us1 ON us1.id = CAST(rm.created_by AS UUID)
LEFT JOIN users AS us2 ON us2.id = CAST(rm.updated_by AS UUID)
LEFT JOIN warehouse AS w ON w.id = rm.warehouse_id
WHERE rm.code = :code
"""
