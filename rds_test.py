import logging
import pymysql
import json
import config


def lambda_handler(event, context):
    if event.get("authentication") != "idontknow":
        response = {
            'statusCode': 401,
            'body': json.dumps('Unauthorized'),
        }
        return response

    response = {
        'statusCode': 500,
        'body': json.dumps('Internal server error'),
    }
    # rds settings
    rds_host = "database.cy48cztfhvsr.ap-southeast-2.rds.amazonaws.com"
    username = config.rds_database_username
    password = config.rds_database_password

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    item_count = 0
    table_created = False
    try:
        conn = pymysql.connect(host=rds_host, user=username, passwd=password, connect_timeout=5,
                               port=3306)
        db_connected = True
        response['db_connected'] = db_connected
        logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
    except pymysql.MySQLError as e:
        db_connected = False
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        response['e'] = e
        response['db_connected'] = db_connected
        return response
    try:
        with conn.cursor() as cur:
            cur.execute('CREATE DATABASE IF NOT EXISTS unimate;')
            cur.execute('USE unimate;')
            cur.execute(
                "create table IF NOT EXISTS USER ( uid varchar(255) NOT NULL UNIQUE , username varchar(255) NOT NULL UNIQUE, password varchar(255) NOT NULL)")
            conn.commit()
        table_created = True
        response['table_created'] = table_created
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        response['e'] = e
        response['table_created'] = table_created
        conn.close()
        return response

    if event['sql'] == 'insert':
        if 'uid' not in event or 'username' not in event or 'password' not in event:
            response['body'] = json.dumps('attributes missing')
            conn.close()
            return response
        try:
            with conn.cursor() as cur:
                statement = "insert into USER VALUES ('" + event['uid'] + "','" + event['username'] + "','" + \
                            event['password'] + "')"
                cur.execute(statement)
                logger.info("affected rows = {}".format(cur.rowcount))
                conn.commit()
            conn.commit()
            response['statusCode'] = 200
            response['status'] = 'success'
            conn.close()
            return response
        except pymysql.MySQLError as e:
            logger.error(e)
            response['e'] = e
            conn.close()
            return response

    elif event['sql'] == 'update':
        if 'uid' not in event or 'password' not in event:
            response['body'] = json.dumps('attributes missing')
            conn.close()
            return response
        try:
            with conn.cursor() as cur:
                statement = "UPDATE USER SET password = %s WHERE uid = %s"
                val = (event['password'], event['uid'])
                cur.execute(statement, val)
                logger.info("affected rows = {}".format(cur.rowcount))
                conn.commit()
            conn.commit()
            response['statusCode'] = 200
            response['status'] = 'success'
            conn.close()
            return response
        except pymysql.MySQLError as e:
            logger.error(e)
            response['e'] = e
            conn.close()
            return response

    elif event['sql'] == 'select':
        try:
            item = []
            with conn.cursor() as cur:
                cur.execute("select * from USER")
                for row in cur:
                    item.append(row)
                    item_count += 1
                    # logger.info(row)
                    # print(row)
            conn.commit()
            response['row'] = item
            response['statusCode'] = 200
            response['status'] = 'success'
            conn.close()
            return response
        except pymysql.MySQLError as e:
            logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
            logger.error(e)
            response['e'] = e
            conn.close()
            return response

    elif event['sql'] == 'delete':
        try:
            with conn.cursor() as cur:
                cur.execute('DROP DATABASE unimate;')
                conn.commit()

            response['statusCode'] = 200
            response['status'] = 'success'
            conn.close()
            return response
        except pymysql.MySQLError as e:
            db_connected = False
            logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
            logger.error(e)
            response['e'] = e
            conn.close()
            return response

    elif event['sql'] == 'show':
        try:
            with conn.cursor() as cur:
                cur.execute("DESCRIBE USER")
                l = cur.fetchall()
                response['cur'] = l
            conn.commit()
            response['statusCode'] = 200
            response['status'] = 'success'
            conn.close()
            return response
        except pymysql.MySQLError as e:
            db_connected = False
            logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
            logger.error(e)
            response['e'] = e
            conn.close()
            return response
    elif event['sql'] == 'check':
        if 'username' not in event or 'password' not in event:
            response['body'] = json.dumps('attributes missing')
            conn.close()
            return response
        try:
            item = []
            with conn.cursor() as cur:
                statement = "select * from USER where username = %s"
                val = event['username']
                cur.execute(statement, val)
                for row in cur:
                    item.append(row)
                    item_count += 1
                    # logger.info(row)
                    # print(row)
            conn.commit()
            if not item:
                response['check'] = False
                response['username'] = False
                conn.close()
                return response
            if event['username'] != item[0][1] or event['password'] != item[0][2]:
                response['check'] = False
                conn.close()
                return response
            response['check'] = True
            response['uid'] = item[0][0]
            response['statusCode'] = 200
            response['status'] = 'success'
            response['body'] = ''
            conn.close()
            return response
        except pymysql.MySQLError as e:
            logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
            logger.error(e)
            response['e'] = e
            conn.close()
            return response

    else:
        response['body'] = json.dumps('SQL command error')
        conn.close()
        return response
    # return "Added %d items from RDS MySQL table" % (item_count)
