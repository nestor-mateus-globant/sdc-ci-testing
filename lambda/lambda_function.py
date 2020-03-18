import json
import sys
import mysql.connector
from mysql.connector import errorcode

def lambda_handler(event, context):
    # TODO implement
    print("[INFO]  Received event: " + json.dumps(event, indent=2))
    try :
        response = getattr(sys.modules[__name__], event['type'])(event['body'])
    except Exception as err:
        raise Exception(err)
    return {
        'statusCode': 200,
        'body': json.dumps(response)
        
    }


def get_cur(arr) :
    try:
      cnx = mysql.connector.connect(user=arr['uname'],password=arr['pwd'],host=arr['host'])
      return cnx
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        return "Database does not exist"
      else:
        return err
    


def getClientCredentials(body) :
    cnx    = get_cur(body)
    cur    = cnx.cursor(dictionary=True)    
    cur.execute("SELECT * FROM pwbi.pwbi_config")
    result = cur.fetchone()
    cur.close()
    cnx.close()
    return result
    
def ListWorkSpaces(body) :
  cnx    = get_cur(body)
  cur    = cnx.cursor(dictionary=True)
  cur.execute("SELECT * FROM pwbi.pwbi_groups where client_id = '{}' ".format(body['where']['client_id']))
  records = cur.fetchall()
  result = []
  for row in records:
    result.append(row)
  cur.close()
  cnx.close()
  return result
  
def ListDatasets(body) :
  cnx    = get_cur(body)
  cur    = cnx.cursor(dictionary=True)
  cur.execute("SELECT * FROM pwbi.pwbi_datasets where group_id = '{}' ".format(body['where']['group_id']))
  records = cur.fetchall()
  result = []
  for row in records:
    result.append(row)
  cur.close()
  cnx.close()
  return result
  
def Getreports(body) :
  cnx    = get_cur(body)
  cur    = cnx.cursor(dictionary=True)
  cur.execute("SELECT * FROM pwbi.pwbi_reports where  group_id = '{}' ".format(body['where']['group_id']))
  records = cur.fetchall()
  result = []
  for row in records:
    result.append(row)
  cur.close()
  cnx.close()
  return result
  
def GetreportbyName(body) :
  cnx    = get_cur(body)
  cur    = cnx.cursor(dictionary=True)
  cur.execute("SELECT * FROM pwbi.pwbi_reports where group_id = '{}' and lower(report_name) like '%{}%'  ".format(body['where']['group_id'],body['where']['report_name'].lower()))
  records = cur.fetchall()
  result = []
  for row in records:
    result.append(row)
  cur.close()
  cnx.close()
  return result
  
def UpdateReport(body):
  cnx    = get_cur(body)
  cur    = cnx.cursor(dictionary=True)
  cur.execute("update pwbi.pwbi_reports set settings = '{}', report_name = '{}', client_id = '{}', group_id= '{}' where report_id = '{}'  ".format(
    body['update']['settings'],body['update']['report_name'],body['update']['client_id'],body['update']['group_id'],body['where']['report_id']))
  result = []
  result.append(cur.rowcount)
  cnx.commit()
  cur.close()
  cnx.close()
  return result
  
  
def DeleteReport(body):
  cnx    = get_cur(body)
  cur    = cnx.cursor(dictionary=True)
  cur.execute("delete from  pwbi.pwbi_reports where report_id = '{}'  ".format(body['where']['report_id']))
  result = []
  result.append(cur.rowcount)
  cnx.commit()
  cur.close()
  cnx.close()
  return result


def CreateReport(body):
  cnx    = get_cur(body)
  cur    = cnx.cursor(dictionary=True)
  cur.execute("insert into pwbi.pwbi_reports (client_id,group_id,report_id,report_name,settings) values ('{}','{}','{}','{}','{}')  ".format(body['insert']['client_id'],body['insert']['group_id'],body['insert']['report_id'],body['insert']['report_name'],body['insert']['settings']))
  result = []
  result.append(cur.rowcount)
  cnx.commit()
  cur.close()
  cnx.close()
  return result