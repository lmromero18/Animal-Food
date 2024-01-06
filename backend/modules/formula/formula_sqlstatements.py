CREATE_FORMULA_ITEM = """ 
INSERT INTO formula (id, is_active, created_at, updated_at, created_by, updated_by, required_quantity, product_id, raw_material_id) 
VALUES (:id, :is_active, :created_at, :updated_at, :created_by, :updated_by,  :required_quantity, :product_id, :raw_material_id) 
RETURNING id, is_active, created_at, updated_at, created_by, updated_by, required_quantity, product_id, raw_material_id; 
"""

GET_FORMULA_LIST = """
SELECT p.id, p.required_quantity, p.is_active, p.created_at, p.updated_at,
CAST(p.created_by AS UUID) AS created_by,
CAST(p.updated_by AS UUID) AS updated_by,
us1.fullname AS created_by_name,
us2.fullname AS updated_by_name,
pr.id AS product_id,
pr.name AS product_name,
rm.id AS raw_material_id,
rm.name AS raw_material_name
FROM formula AS p
LEFT JOIN users AS us1 ON us1.id = CAST(p.created_by AS UUID)
LEFT JOIN users AS us2 ON us2.id = CAST(p.updated_by AS UUID)
LEFT JOIN product AS pr ON pr.id = p.product_id
LEFT JOIN rawmaterial AS rm ON rm.id = p.raw_material_id
"""

def formula_list_search():
    return """ WHERE (pr.name LIKE :search) """

def formula_list_complements(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY pr.name ASC;"
    elif order == "name" and direction == "DESC":
        sql_sentence = " ORDER BY pr.name DESC;"
    elif order == "name" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY pr.name ASC;"
    elif order == "status" and direction == "DESC":
        sql_sentence = " ORDER BY pr.is_active DESC;"
    elif order == "status" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY pr.is_active ASC;"

    return sql_sentence

GET_FORMULA_BY_ID = """
SELECT p.id, p.required_quantity, p.is_active, p.created_at, p.updated_at,
CAST(p.created_by AS UUID) AS created_by,
CAST(p.updated_by AS UUID) AS updated_by,
us1.fullname AS created_by_name,
us2.fullname AS updated_by_name,
pr.id AS product_id,
pr.name AS product_name,
rm.id AS raw_material_id,
rm.name AS raw_material_name
FROM formula AS p
LEFT JOIN users AS us1 ON us1.id = CAST(p.created_by AS UUID)
LEFT JOIN users AS us2 ON us2.id = CAST(p.updated_by AS UUID)
LEFT JOIN product AS pr ON pr.id = p.product_id
LEFT JOIN rawmaterial AS rm ON rm.id = p.raw_material_id
WHERE p.id = :id; 
"""

UPDATE_FORMULA_BY_ID = """
    UPDATE formula
    SET product_id = :product_id,
        raw_material_id = :raw_material_id,
        required_quantity = :required_quantity,
        is_active = :is_active,
        created_at = :created_at,
        updated_at = :updated_at,
        created_by = :created_by,
        updated_by = :updated_by
    WHERE id = :id
    RETURNING id, product_id, raw_material_id, required_quantity, is_active, created_at, updated_at, created_by, updated_by;
"""

DELETE_FORMULA_BY_ID = """
    DELETE FROM formula
    WHERE id = :id
    RETURNING id;
"""
