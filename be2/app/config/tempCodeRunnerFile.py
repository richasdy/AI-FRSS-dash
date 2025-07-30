import sqlite3
con = sqlite3.connect("C:\magang\AI-FRSS-dash\mobile.db")

c = con.execute("select * from attendance_logs")
for row in c: 
    print("Data berhasil ditambahkan ke attendance_logs:")
    print(f"Log ID     : {row[0]}")
    print(f"User ID    : {row[1]}")
    print(f"Device ID  : {row[2]}")
    print(f"Check Type : {row[3]}")
    print(f"Confidence : {row[4]}")
    print(f"Timestamp  : {row[5]}")

c = con.execute("select * from users")
for latest_user in c:
    print("User berhasil ditambahkan:")
    print(f"ID: {latest_user[0]}")
    print(f"Name: {latest_user[1]}")
    print(f"Email: {latest_user[2]}")
    print(f"Phone: {latest_user[3]}")
    print(f"Face Embedding: {latest_user[4]}")
    print(f"Photo URL: {latest_user[5]}")
    print(f"Role: {latest_user[6]}")
    print(f"Created At: {latest_user[7]}")
    print(f"Updated At: {latest_user[8]}")
    con.close()