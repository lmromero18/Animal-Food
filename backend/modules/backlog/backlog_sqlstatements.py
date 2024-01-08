CREATE_BACKLOG_ITEM = """ 
INSERT INTO backlog (id, product_id, required_quantity, is_active, created_by, created_at, updated_by, updated_at) 
VALUES(:id, :product_id, :required_quantity, :is_active, :created_by, :created_at, :updated_by, :updated_at) 
RETURNING id, product_id, required_quantity, is_active, created_by, created_at, updated_by, updated_at; """

GET_BACKLOG_LIST = """
    SELECT b.id, b.product_id, b.required_quantity, b.is_active, b.created_at, b.updated_at, 
        CAST(b.created_by AS UUID) AS created_by, 
        CAST(b.updated_by AS UUID) AS updated_by,
        us1.fullname AS created_by_name, 
        us2.fullname AS updated_by_name
    FROM backlog AS b
    LEFT JOIN users AS us1 ON us1.id = CAST(b.created_by AS UUID)
    LEFT JOIN users AS us2 ON us2.id = CAST(b.updated_by AS UUID)
    WHERE b.is_active = true
"""

def backlog_list_search():
    return """ WHERE (b.product_id LIKE :search) """

def backlog_list_complements(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY b.product_id ASC;"
    elif order == "product_id" and direction == "DESC":
        sql_sentence = " ORDER BY b.product_id DESC;"
    elif order == "product_id" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY b.product_id ASC;"
    elif order == "status" and direction == "DESC":
        sql_sentence = " ORDER BY b.is_active DESC;"
    elif order == "status" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY b.is_active ASC;"

    return sql_sentence

GET_BACKLOG_BY_ID = """
    SELECT t.id, t.product_id, t.required_quantity, t.is_active, t.created_by, t.created_at, t.updated_at, 
        t.created_by, t.updated_by
    FROM backlog AS t
    WHERE t.id = :id; 
"""

UPDATE_BACKLOG_BY_ID = """
    UPDATE backlog
    SET product_id     = :product_id,
        required_quantity     = :required_quantity,
        is_active     = :is_active,
        created_by    = :created_by,
        created_at    = :created_at,
        updated_by    = :updated_by,
        updated_at    = :updated_at
    WHERE id = :id
    RETURNING id, product_id, required_quantity, is_active, created_by, created_at, updated_by, updated_at;
"""
DELETE_BACKLOG_BY_ID = """
    DELETE FROM backlog
    WHERE id = :id
    RETURNING id;
"""
GET_BACKLOG_BY_PRODUCT_ID = """
    SELECT t.id, t.product_id, t.required_quantity, t.is_active, t.created_by, t.created_at, t.updated_at, 
        t.created_by, t.updated_by
    FROM backlog AS t
    WHERE t.product_id = :product_id AND t.is_active = true;
"""

UPDATE_BACKLOG_BY_PRODUCT_ID = """
    UPDATE backlog
    SET 
        product_id     = :product_id,
        required_quantity     = :required_quantity,
        is_active     = :is_active,
        created_by    = :created_by,
        created_at    = :created_at,
        updated_by    = :updated_by,
        updated_at    = :updated_at
    WHERE product_id = :product_id AND is_active = true AND id = :id
    RETURNING product_id, required_quantity, is_active, created_by, created_at, updated_by, updated_at;
"""
