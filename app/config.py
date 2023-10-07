from dbutils.pooled_db import PooledDB
import pymysql
import datetime
import logging
import os


# 通过https://my.telegram.org/auth登录telegram账号后注册application，获得api id和api hash
api_id = 100000
api_hash = 'api_hash'
# 监听群消息中的关键字
keywords = ['telegram']
# 匹配到用户发送包含关键字的消息时，向用户发送的消息内容
message = 'hello, test'
# 是否自动向符合条件的用户发送消息，默认为自动发送
auto_send = True
# telegram session文件名，可不做修改
session_name = 'session_name'


pool = PooledDB(
    creator=pymysql,
    host='127.0.0.1',
    mincached=2,
    maxconnections=50,
    blocking=True,
    port=3306,
    user='root',
    password=os.getenv("MYSQL_ROOT_PASSWORD"),
    database='tg_message'
)

logging.basicConfig(format='%(levelname)s: %(asctime)s: %(message)s', filename='log.log', filemode='a', encoding='utf-8', level=logging.INFO)


def custom_decoder(dct):
    return {int(k): v for k, v in dct.items()}


def save_message(sender_id, sender_name, username, group_username, message, send_flag, sender):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = "insert into message (sender_id,sender_name,username,group_username,message,send_flag,sender,date_time) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        current_time = datetime.datetime.now()
        cursor.execute(sql,
                       (sender_id, sender_name, username, group_username, message, send_flag, sender, current_time))
        conn.commit()
    except Exception as e:
        logging.error("insert faild")
        logging.exception(e)
    finally:
        cursor.close()
        conn.close()


def get_total(data, startTime, endTime):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = f"select count(*) from message where TRUE"
        for each in data.keys():
            if data[each]:
                sql = sql + f" and {each}={data[each]}"
        if startTime and endTime:
            sql = sql + f" and date_time < {endTime} and date_time > {startTime}"
        cursor.execute(sql)
        result = cursor.fetchone()
        return result[0]
    except Exception as e:
        logging.error("get total error")
        logging.exception(e)
    finally:
        cursor.close()
        conn.close()


def query_message(current, pageSize, data, startTime, endTime):
    conn = pool.connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        sql = f"select id,sender_id,sender_name,username,group_username,message,send_flag,date_format(date_time, '%Y-%m-%d %H:%i:%s') as created_at from message where TRUE"
        for each in data.keys():
            if data[each]:
                sql = sql + f" and {each}={data[each]}"
        if startTime and endTime:
            sql = sql + f" and date_time <= '{endTime} 23:59:59' and date_time >= '{startTime} 00:00:00'"
        sql = sql + f" limit {pageSize} offset {(current - 1) * pageSize}"
        cursor.execute(sql)
        result = cursor.fetchall()
        total = get_total(data, startTime, endTime)
        return result, total
    except Exception as e:
        logging.error("query message error")
        logging.exception(e)
    finally:
        cursor.close()
        conn.close()


def get_sender(id):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = f"select sender from message where id={id}"
        cursor.execute(sql)
        result = cursor.fetchone()
        return result[0]
    except Exception as e:
        logging.error("get sender error")
        logging.exception(e)
        return False
    finally:
        cursor.close()
        conn.close()


def update_message(id, send_flag):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = f"update message set send_flag='{send_flag}',date_time='{datetime.datetime.now()}' where id={id}"
        cursor.execute(sql)
        conn.commit()
        return True
    except Exception as e:
        logging.error("update message error")
        logging.exception(e)
        return False
    finally:
        cursor.close()
        conn.close()
