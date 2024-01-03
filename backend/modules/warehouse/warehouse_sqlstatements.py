CREATE_WAREHOUSE_ITEM = """ 
INSERT INTO warehouse (id, type, number, is_active, name, created_by, created_at, updated_by, updated_at) 
VALUES(:id, :type, :number, :is_active, :name, :created_by, :created_at, :updated_by, :updated_at) 
RETURNING id, type, number, is_active, name, created_by, created_at, updated_by, updated_at; """

GET_WAREHOUSE_LIST = """
    SELECT w.id, w.type, w.name, w.is_active, w.created_at, w.updated_at, 
        CAST(w.created_by AS UUID) AS created_by, 
        CAST(w.updated_by AS UUID) AS updated_by,
        us1.fullname AS created_by_name, 
        us2.fullname AS updated_by_name
    FROM warehouse AS w
    LEFT JOIN users AS us1 ON us1.id = CAST(w.created_by AS UUID)
    LEFT JOIN users AS us2 ON us2.id = CAST(w.updated_by AS UUID)
"""

def warehouse_list_search():
    return """ WHERE (w.name LIKE :search) """

def warehouse_list_complements(order: str | None, direction: str | None):
    sql_sentence = ""
    if not order and not direction:
        sql_sentence = " ORDER BY w.name ASC;"
    elif order == "name" and direction == "DESC":
        sql_sentence = " ORDER BY w.name DESC;"
    elif order == "name" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY w.name ASC;"
    elif order == "status" and direction == "DESC":
        sql_sentence = " ORDER BY w.is_active DESC;"
    elif order == "status" and (direction == "ASC" or direction == None):
        sql_sentence = " ORDER BY w.is_active ASC;"

    return sql_sentence

GET_WAREHOUSE_BY_ID = """
    SELECT t.id, t.type ,t.name, t.is_active, t.created_by, t.created_at, t.updated_at, 
        t.created_by, t.updated_by
    FROM warehouse AS t
    WHERE t.id = :id; 
"""

UPDATE_WAREHOUSE_BY_ID = """
    UPDATE warehouse
    SET type     = :type,
        name     = :name,
        is_active     = :is_active,
        created_by    = :created_by,
        created_at    = :created_at,
        updated_by    = :updated_by,
        updated_at    = :updated_at
    WHERE id = :id
    RETURNING id, type, is_active, created_by, created_at, updated_by, updated_at;
"""
DELETE_WAREHOUSE_BY_ID = """
    DELETE FROM warehouse
    WHERE id = :id
    RETURNING id;
"""