import requests
import pymysql

def fetch_sql_from_github(repo_url, file_path):
    raw_url = f"{repo_url}/raw/main/{file_path}"  # Adjust 'main' to the branch where the file is located
    try:
        response = requests.get(raw_url)
        if response.status_code == 200:
            sql_script = response.text
            return sql_script
        else:
            print(f"Failed to fetch SQL file from GitHub. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SQL file from GitHub: {e}")
        return None

def execute_sql_on_rds(sql_script, rds_host, rds_user, rds_password, rds_database):
    try:
        connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_database)
        cursor = connection.cursor()
        cursor.execute(sql_script)
        connection.commit()
        print("Database deployed successfully!")
    except Exception as e:
        print(f"Error executing SQL script on RDS: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    # Set your GitHub repository URL and file path details here
    github_repo_url = 'https://github.com/gcarvalhoUC/ER-SQLDatabase'
    github_file_path = 'erplus.sql'  
    rds_host = 'erplus-withdb-rdsinstance-jpwfterttovm.czgkzxn4tyv0.us-east-2.rds.amazonaws.com'
    rds_user = 'admin'
    rds_password = 'admin1234567'
    rds_database = 'tpchUsecase'

    sql_script = fetch_sql_from_github(github_repo_url, github_file_path)
    if sql_script:
        print(sql_script)
        execute_sql_on_rds(sql_script, rds_host, rds_user, rds_password, rds_database)

