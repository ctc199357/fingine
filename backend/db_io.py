import os
from dotenv import load_dotenv

import sqlite3

load_dotenv()

created_by_current = os.getenv('CREATED_BY')
create_extraction = """
CREATE TABLE IF NOT EXISTS "EXTRACTION" (
  "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
  "IMAGE_ID" INTEGER NOT NULL,
  "DATE_OF_SPENDING" TEXT DEFAULT NULL,
  "LOCATION_OF_SPENDING" TEXT DEFAULT NULL,
  "SPENDING_COMPANY" TEXT DEFAULT NULL,
  "DOLLAR_SPENT" REAL DEFAULT NULL,
  "ITEMS_OR_SERVICE_BOUGHT" TEXT,
  "CATEGORY" TEXT DEFAULT NULL,
  "EXTRACTION_METHOD" TEXT,
  "EXTRACTION_STATUS" TEXT,
  "EXTRACTION_DATE" TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "CREATED_BY" TEXT NOT NULL,
  "CREATED_DATE" TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "UPDATED_BY" TEXT DEFAULT NULL,
  "UPDATED_DATE" TEXT DEFAULT NULL,
  FOREIGN KEY ("IMAGE_ID") REFERENCES "IMAGES" ("ID")
);
"""
create_extraction_2 = """CREATE INDEX IF NOT EXISTS idx_extraction_image_id ON "EXTRACTION" ("IMAGE_ID");"""


create_image = """
CREATE TABLE IF NOT EXISTS "IMAGES" (
  "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
  "IMAGE_DATA" BLOB NOT NULL,
  "IMAGE_NAME" TEXT NOT NULL,
  "FILE_TYPE" TEXT NOT NULL,
  "UPLOAD_DATE" TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "IMAGE_SIZE" INTEGER NOT NULL,
  "CONTENT_TYPE" TEXT NOT NULL,
  "CREATED_BY" TEXT NOT NULL,
  "CREATED_DATE" TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "UPDATED_BY" TEXT,
  "UPDATED_DATE" TEXT
);
"""

def connect_to_db():
    # cnx = mysql.connector.connect(
    #     user=os.getenv('sql_user'),
    #     password=os.getenv('sql_password'),
    #     host=os.getenv('sql_url'),
    #     port = int(os.getenv('sql_port')),
    #     database=os.getenv('db')
    # )
    # cursor = cnx.cursor()
    cnx = sqlite3.connect('poc_db.db')
    cursor = cnx.cursor() 
    cursor.execute(create_image)
    cursor.execute(create_extraction)
    cursor.execute(create_extraction_2)
    return cnx, cursor

def close_cnx_cursor(cnx, cursor):
    return cursor.close(), cnx.close()

def insert_extraction(image_id, date_of_spending, location_of_spending, spending_company, dollar_spent, items_or_service_bought, category, extraction_method, extraction_status,
                      created_by):
    
    cnx, cursor = connect_to_db()
    
    # query = """
    #     INSERT INTO EXTRACTION (
    #         IMAGE_ID,
    #         DATE_OF_SPENDING,
    #         LOCATION_OF_SPENDING,
    #         SPENDING_COMPANY,
    #         DOLLAR_SPENT,
    #         ITEMS_OR_SERVICE_BOUGHT,
    #         CATEGORY,
    #         EXTRACTION_METHOD,
    #         EXTRACTION_STATUS,
    #         EXTRACTION_DATE,
    #         CREATED_BY,
    #         CREATED_DATE
    #     ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, NOW())
    # """
    # params = (
    #     image_id,
    #     date_of_spending,
    #     location_of_spending,
    #     spending_company,
    #     dollar_spent,
    #     items_or_service_bought,
    #     category,
    #     extraction_method,
    #     extraction_status,
    #     created_by
    # )


    query = """
        INSERT INTO EXTRACTION (
            IMAGE_ID,
            DATE_OF_SPENDING,
            LOCATION_OF_SPENDING,
            SPENDING_COMPANY,
            DOLLAR_SPENT,
            ITEMS_OR_SERVICE_BOUGHT,
            CATEGORY,
            EXTRACTION_METHOD,
            EXTRACTION_STATUS,
            EXTRACTION_DATE,
            CREATED_BY,
            CREATED_DATE
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?, CURRENT_TIMESTAMP)
    """
    params = (
        image_id,
        date_of_spending,
        location_of_spending,
        spending_company,
        dollar_spent,
        items_or_service_bought,
        category,
        extraction_method,
        extraction_status,
        created_by
    )

    cursor.execute(query, params)

    extraction_id = cursor.lastrowid
    
    cnx.commit()

    close_cnx_cursor(cnx, cursor)

    return extraction_id
    
def insert_image(image_data, image_name, file_type, upload_date, image_size, content_type, created_by):
    
    cnx, cursor = connect_to_db()
    # query = """
    #     INSERT INTO IMAGES (
    #         IMAGE_DATA,
    #         IMAGE_NAME,
    #         FILE_TYPE,
    #         UPLOAD_DATE,
    #         IMAGE_SIZE,
    #         CONTENT_TYPE,
    #         CREATED_BY,
    #         CREATED_DATE
    #     ) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
    # """

    query = """
        INSERT INTO IMAGES (
            IMAGE_DATA,
            IMAGE_NAME,
            FILE_TYPE,
            UPLOAD_DATE,
            IMAGE_SIZE,
            CONTENT_TYPE,
            CREATED_BY,
            CREATED_DATE
        ) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """
    params = (
        image_data,
        image_name,
        file_type,
        upload_date,
        image_size,
        content_type,
        created_by
    )
    cursor.execute(query, params)
    image_id = cursor.lastrowid
    cnx.commit()
    close_cnx_cursor(cnx, cursor)
    return image_id

def select_extraction(created_by):
    
    cnx, cursor = connect_to_db()
    query = """
        SELECT
            ID, 
            IMAGE_ID,
            DATE_OF_SPENDING,
            LOCATION_OF_SPENDING,
            SPENDING_COMPANY,
            DOLLAR_SPENT,
            CATEGORY FROM EXTRACTION 
        WHERE CREATED_BY = ?
    """
    params = (created_by,)
    cursor.execute(query, params)
    results = cursor.fetchall()
    close_cnx_cursor(cnx,cursor)
    return results

def select_image(IMAGE_IDS):
    
    cnx, cursor = connect_to_db()
    # query = """
    #     SELECT ID, IMAGE_DATA FROM IMAGES WHERE ID IN (%s)
    # """
    # params = tuple('{}'.format(id) for id in IMAGE_IDS)
    # query = query % ','.join(['%s'] * len(IMAGE_IDS))
    query = """
        SELECT ID, IMAGE_DATA FROM IMAGES WHERE ID IN ({})
    """.format(','.join(['?'] * len(IMAGE_IDS)))

    params = IMAGE_IDS

    cursor.execute(query, params)
    results = cursor.fetchall()
    print(results)
    close_cnx_cursor(cnx,cursor)
    return results


def update_extraction(extraction_id, date_of_spending, location_of_spending, spending_company, dollar_spent, category, updated_by):
    cnx, cursor = connect_to_db()

    # query = """
    #     UPDATE EXTRACTION
    #     SET 
    #         DATE_OF_SPENDING = %s,
    #         LOCATION_OF_SPENDING = %s,
    #         SPENDING_COMPANY = %s,
    #         DOLLAR_SPENT = %s,
    #         CATEGORY = %s,
    #         UPDATED_DATE = NOW(),
    #         UPDATED_BY = %s
    #     WHERE ID = %s
    # """
    # params = (
    #     date_of_spending,
    #     location_of_spending,
    #     spending_company,
    #     dollar_spent,
    #     category,
    #     updated_by,
    #     extraction_id
    # )
    query = """
        UPDATE EXTRACTION
        SET 
            DATE_OF_SPENDING = ?,
            LOCATION_OF_SPENDING = ?,
            SPENDING_COMPANY = ?,
            DOLLAR_SPENT = ?,
            CATEGORY = ?,
            UPDATED_DATE = CURRENT_TIMESTAMP,
            UPDATED_BY = ?
        WHERE ID = ?
    """
    params = (
        date_of_spending,
        location_of_spending,
        spending_company,
        dollar_spent,
        category,
        updated_by,
        extraction_id
    )
    cursor.execute(query, params)
    cnx.commit()

    rows_affected = cursor.rowcount

    close_cnx_cursor(cnx, cursor)

    return rows_affected