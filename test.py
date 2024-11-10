import mysql.connector

mysql_url = "mysql://root:EAnDoELmcbiofXxjkVmUZoOsklrbBIno@junction.proxy.rlwy.net:30982/railway"

try:
    db_config = mysql_url.split("://")[1].split("@")
    user_pass = db_config[0].split(":")
    host_port_db = db_config[1].split("/")
    host_port = host_port_db[0].split(":")

    # Establish connection to the Railway MySQL database
    mydb = mysql.connector.connect(
        host=host_port[0],
        user=user_pass[0],
        password=user_pass[1],
        port=host_port[1],
        database=host_port_db[1]
    )

    print("Database connection successful!")

    cursor = mydb.cursor(dictionary=True)

    ic = "900101145678"

    cursor.execute("SELECT * FROM admin WHERE admin_ic=%s", (ic,))
    testval = cursor.fetchone()
    print(testval)

except Exception as e:
    print(f"Error connecting to the database: {e}")