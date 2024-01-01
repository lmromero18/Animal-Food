CREATE_WAREHOUSE_ITEM = """ 
INSERT INTO warehouse (id, type, number, is_active, name, created_by, created_at, updated_by, updated_at) 
VALUES(:id, :type, :number, :is_active, :name, :created_by, :created_at, :updated_by, :updated_at) 
RETURNING id, type, number, is_active, name, created_by, created_at, updated_by, updated_at; """