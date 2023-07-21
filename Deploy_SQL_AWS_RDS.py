import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import boto3


# try:
#     print("TRY CONNECTION #1 (Cloud)")

#     connection = mysql.connector.connect(
#         host='erplus-withdb-rdsinstance-jpwfterttovm.czgkzxn4tyv0.us-east-2.rds.amazonaws.com', port= '3306', user='admin', password='admin1234567', database='tpchUsecase')

#     print("CONNECTED\n")

#     cursor_Cl = connection.cursor()
	
# 	for line in open(PATH_TO_FILE):
# 		cursor.execute(line)
	

#     data_byDay_AVG_last_timestamp = cursor_Cl_AVG.fetchone()

#     connection.commit()
#     print("Record read successfully from data_byDay_AVG table")
#     cursor_Cl_AVG.close()

# except mysql.connector.Error as error:
#     print("Failed to read record from data_byDay_AVG table {}".format(error))

# finally:
#     if (connection.is_connected()):
#         connection.close()
#         print("MySQL connection is closed")



def connect_to_mysql(host, user, password, database):
    """
    Connects to a MySQL database.

    Args:
        host: The hostname of the MySQL server.
        user: The username for the MySQL database.
        password: The password for the MySQL database.
        database: The name of the MySQL database.

    Returns:
        A connection to the MySQL database.
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection
    except mysql.connector.Error as error:
        print("Failed to read record from data_byDay_AVG table {}".format(error))

def run_sql_file_from_s3(connection, bucket, key):
    """
    Runs a SQL file on a MySQL database from S3.

    Args:
        connection: A connection to the MySQL database.
        bucket: The name of the S3 bucket.
        key: The key of the SQL file in the S3 bucket.

    Returns:
        None.
    """

    s3 = boto3.resource("s3")

    with s3.Object(bucket, key).open() as sql_file:
        sql_script = sql_file.read()

    connection.cursor().execute(sql_script)
    connection.commit()

if __name__ == "__main__":
    host = "erplus-withdb-rdsinstance-jpwfterttovm.czgkzxn4tyv0.us-east-2.rds.amazonaws.com"
    user = "admin"
    password = "admin1234567"
    database = "tpchUsecase"
    bucket = "erplus-sql"
    key = "erplus.sql"

    connection = connect_to_mysql(host, user, password, database)
    run_sql_file_from_s3(connection, bucket, key)

    if (connection.is_connected()):
        connection.close()
        print("MySQL connection is closed")
