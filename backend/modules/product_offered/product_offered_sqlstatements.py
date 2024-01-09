CREATE_PRODUCT_OFFERED_ITEM = """ 
INSERT INTO product_offered (id, name, code ,quantity, is_active, created_at, updated_at, created_by, updated_by, warehouse_id, product_id) 
VALUES (:id, :name, :code, :quantity,  :is_active, :created_at, :updated_at, :created_by, :updated_by, :warehouse_id, :product_id) 
RETURNING id, name, code, quantity, is_active, created_at, updated_at, created_by, updated_by, warehouse_id, product_id; 
"""

GET_PRODUCT_OFFERED_LIST = """
    SELECT p.id, p.name, p.code, p.quantity, p.is_active, p.created_at, p.updated_at, 
        CAST(p.created_by AS UUID) AS created_by, 
        CAST(p.updated_by AS UUID) AS updated_by,
        us1.fullname AS created_by_name, 
        us2.fullname AS updated_by_name,
        w.id AS warehouse_id,
        w.name AS warehouse_name,
        pr.id AS product_id,
        pr.name AS product_offered_name
    FROM product_offered AS p
    LEFT JOIN users AS us1 ON us1.id = CAST(p.created_by AS UUID)
    LEFT JOIN users AS us2 ON us2.id = CAST(p.updated_by AS UUID)
    LEFT JOIN warehouse AS w ON w.id = p.warehouse_id
    LEFT JOIN product AS pr ON pr.id = p.product_id
"""

def product_offered_list_search():
    return """ WHERE (p.code LIKE :search) """

def product_offered_list_complements(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY p.code ASC;"
    elif order == "code" and direction == "DESC":
        sql_sentence = " ORDER BY p.code DESC;"
    elif order == "code" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY p.code ASC;"
    elif order == "status" and direction == "DESC":
        sql_sentence = " ORDER BY p.is_active DESC;"
    elif order == "status" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY p.is_active ASC;"

    return sql_sentence

GET_PRODUCT_OFFERED_BY_ID = """
    SELECT p.id, p.name, p.code, p.quantity, p.is_active, p.created_at, p.updated_at, 
        CAST(p.created_by AS UUID) AS created_by, 
        CAST(p.updated_by AS UUID) AS updated_by,
        us1.fullname AS created_by_name, 
        us2.fullname AS updated_by_name,
        w.id AS warehouse_id,
        w.name AS warehouse_name,
        pr.id AS product_id,
        pr.name AS product_offered_name
    FROM product_offered AS p
    LEFT JOIN users AS us1 ON us1.id = CAST(p.created_by AS UUID)
    LEFT JOIN users AS us2 ON us2.id = CAST(p.updated_by AS UUID)
    LEFT JOIN warehouse AS w ON w.id = p.warehouse_id
    LEFT JOIN product AS pr ON pr.id = p.product_id
    WHERE p.id = :id; 
"""

UPDATE_PRODUCT_OFFERED_BY_ID = """
    UPDATE product_offered
    SET name = :name,
        quantity = :quantity,
        code = :code,
        is_active = :is_active,
        created_at = :created_at,
        updated_at = :updated_at,
        created_by = :created_by,
        updated_by = :updated_by,
        warehouse_id = :warehouse_id,
        product_id = :product_id
    WHERE id = :id
    RETURNING id, name, code, quantity, is_active, created_at, updated_at, created_by, updated_by, warehouse_id, product_id;
"""

DELETE_PRODUCT_OFFERED_BY_ID = """
    DELETE FROM product_offered
    WHERE id = :id
    RETURNING id;
"""

CHECK_FORMULA_REQUIREMENTS = """
WITH formula_requirements AS (
    SELECT
        f.raw_material_id,
        f.required_quantity * :product_quantity AS total_required_quantity,
        r.available_quantity,
        r.name AS raw_material_name,
        (f.required_quantity * :product_quantity - r.available_quantity) AS quantity_missing
    FROM formula f JOIN
    rawmaterial r ON f.raw_material_id = r.id
    WHERE f.product_id = :product_id),
    requirements_not_met AS (
    SELECT * FROM formula_requirements WHERE quantity_missing > 0),
    update_requirements AS (
    SELECT
        raw_material_id,
        available_quantity - total_required_quantity AS new_quantity
    FROM formula_requirements
    WHERE NOT EXISTS (SELECT 1 FROM requirements_not_met)
),
update_rawmaterial AS (
    UPDATE rawmaterial
    SET available_quantity = update_requirements.new_quantity
    FROM update_requirements
    WHERE rawmaterial.id = update_requirements.raw_material_id
    RETURNING *)
SELECT CASE
    WHEN EXISTS (SELECT 1 FROM requirements_not_met) THEN 'false'
    WHEN EXISTS (SELECT 1 FROM update_rawmaterial) THEN 'true'
    ELSE 'false'
END;
"""

GET_PRODUCT_OFFERED_BY_NAME = """
    SELECT p.id, p.name, p.code, p.quantity, p.is_active, p.created_at, p.updated_at, 
        CAST(p.created_by AS UUID) AS created_by, 
        CAST(p.updated_by AS UUID) AS updated_by,
        us1.fullname AS created_by_name, 
        us2.fullname AS updated_by_name,
        w.id AS warehouse_id,
        w.name AS warehouse_name,
        pr.id AS product_id,
        pr.name AS product_offered_name
    FROM product_offered AS p
    LEFT JOIN users AS us1 ON us1.id = CAST(p.created_by AS UUID)
    LEFT JOIN users AS us2 ON us2.id = CAST(p.updated_by AS UUID)
    LEFT JOIN warehouse AS w ON w.id = p.warehouse_id
    LEFT JOIN product AS pr ON pr.id = p.product_id
    WHERE p.name = :name; 
"""