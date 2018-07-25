# -*-coding:utf-8-*-
# import sys)

cnn = ''
def Renew():
    global  conn
    conn.commit()

print(type(cnn))
cnn.execute("select keyword,time,input_id from input where status=0;")
print(cnn)