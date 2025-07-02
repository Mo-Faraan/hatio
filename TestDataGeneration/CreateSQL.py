# import oracledb

# csv_file="C:/Users/MYPC/Desktop/hatio/arjun_Tasks/TestDataGeneration/output_xml/transactions_1.csv"
# connection = oracledb.connect(
#     user="TestData",
#     password="farhantm@123",
#     dsn="localhost/FREEPDB1"
# )

# cursor = connection.cursor()
# with open(csv_file, "r", encoding="utf-8") as f:
#     next(f)
#     for line in f:
#         TXNREFID, ABC, DEF, HIJ, LMN = line.strip().split(",")
#         cursor.execute(
#             "INSERT INTO TESTDATA (TXNREFID, ABC, DEF, HIJ, LMN) VALUES (:1, :2, :3, :4, :5)",
#             (TXNREFID, ABC, DEF, HIJ, LMN)
#         )
# connection.commit()
# cursor.close()
# connection.close()

import csv

# List of columns in the correct order as per your table definition
columns = [
    "BC_MASTER_ID", "OBJECT_ID", "SOURCE_ID", "BILLER_ID", "VALID_UNTIL", "VALIDATION_ID",
    "BILLER_REFERENCE_NO", "BILLFETCH_PARAMS", "PAYMENT_ID", "SOURCE_REF_NO", "BBPS_REF_NO",
    "TXN_DATE_TIME", "POSTING_ID", "POSTING_DATE", "STATUS", "RETRY_COUNT", "BILLER_RETRY",
    "CREATED_AT", "UPDATED_AT", "CREATED_BY", "UPDATED_BY", "BOU_REQ_RESP_ID", "VALIDATION_DATE",
    "TRACE_ID", "BILLER_CONNECT_RETRY", "REQ_BD_TIMESTAMP", "BILL_DATE", "BILL_DUE_DATE",
    "BC_ERROR_CODE", "BC_ERROR_MESSAGE", "VENDOR_RRN", "AUTH1", "AUTH2", "AUTH3", "AUTH4",
    "VENDOR_REF_ID", "SUB_DIV_NAME", "BILL_AMOUNT", "BOU_CONV_FEES", "COU_CONV_FEES",
    "MODE_OF_PAYMENT", "BILLER_REQUEST_TYPE", "OUID"
]

def format_value(val):
    if val is None or val == '':
        return "NULL"
    # For Oracle, wrap strings in single quotes and escape single quotes inside
    return f"'{str(val).replace('\'', '\'\'')}'"

csv_file = 'output_xml/transactions_BillerConn_1.csv'  # Change to your CSV file path

with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    st=[]
    for row in reader:
        values = [format_value(row.get(col, '')) for col in columns]
        insert_stmt = f'INSERT INTO TBL_BILLER_CONNECT_MASTER ({", ".join(columns)}) VALUES ({", ".join(values)});'
        # print(insert_stmt)
        st.append(insert_stmt)

for i in range(len(st)):
    print()
    print(st[i])
