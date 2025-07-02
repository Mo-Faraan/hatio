import xml.etree.ElementTree as ET
import random
from datetime import datetime, timedelta, date, timezone
from zoneinfo import ZoneInfo
import os
import string
import csv
import tkinter as tk
from tkinter import messagebox, filedialog

selected_folder = ""
successTxnRefIds = dict()
s=""
BOUTRNREFNO = 0
BillerId = 0

def generate_random_transaction(flag):
    txnDate = date.today().strftime("%Y-%m-%d")
    clearingTimestamp = (datetime.now(timezone(timedelta(hours=5, minutes=30)))).strftime("%Y-%m-%dT%H:%M:%S+05:30")

    characters = string.ascii_uppercase + string.digits
    msgId = random.choice(string.ascii_uppercase) + "".join(random.choices(characters, k=33))
    txnReferenceId = random.choice(string.ascii_uppercase) + "".join(random.choices(characters, k=19))

    settlementCycleId = s

    # billerIds = ["HDFC00000NATW1", "MPPK00000MAP01", "HDFC00000NAT5K", "UTTA00000UTT7M", "MPEZ00000MAP02", "HATHWAY00NAT01", "HDBF00000NATGJ", "TATAPWR00DEL01", "NESCO0000ODI01", "AYEF00000NATZB", "MPCZ00000MAP01", "SOLA00000MAHG9", "MADH00000GUJOY", "ELEC00000CHA3L", "INDI00000NAT26", "MUNI00000CHANI", "LUCK00000LUC9J", "WESCO0000ODI01", "CNHI00000NATNZ", "PATN00000BIHJ3", "FUSI00000DEL5E", "ARTH00000NAT4D", "COMM00000TELQ2", "HUKK00000NATGM"]
    billerId = BillerId

    paymentMode = random.choice(["Internet Banking", "Credit Card", "UPI"])

    success = ["PAYMENT", "FORCE PAYMENT", "FORCE PAYMENT PRE-ARBITRATION", "FORCE PAYMENT PARTIAL GOOD FAITH", "FORCE PAYMENT FULL GOOD FAITH", "FORCE PAYMENT ARBITRATION"]
    refund = ["CREDIT ADJUSTMENT", "REFUND", "REFUND PRE-ARBITRATION", "REFUND PARTIAL GOOD FAITH", "REFUND FULL GOOD FAITH", "REFUND ARBITRATION"]

    if flag=="SUCCESS":
        mti = random.choice(success)
        responseCode = "000"
        txnAmount = str(random.randint(1000, 1000000))
        successTxnRefIds[txnReferenceId]=txnAmount
    elif flag == "REFUND":
        mti = random.choice(refund)
        responseCode = random.choice(["000", "001", "200"])
        txnReferenceId = random.choice(list(successTxnRefIds.keys()))
        txnAmount = "-"+successTxnRefIds[txnReferenceId]
        del successTxnRefIds[txnReferenceId]
    else :
        mti = random.choice(success)
        responseCode = random.choice(["001", "200"])
        txnAmount = "0"

    transaction = {
        "msgId": msgId,
        "refId": msgId,
        "origRefId": "NA",
        "mti": mti,
        "txnReferenceId": txnReferenceId,
        "txnType": "PAYMENT",
        "txnDate": txnDate,
        "customerOUId": random.choice(["PP11", "PP22", "PP33"]),
        "billerOUId": random.choice(["HD51", "JK21", "IF11"]),
        "responseCode": responseCode,
        "txnCurrencyCode": "356",
        "txnAmount": txnAmount,
        "customerConvenienceFee": "0.0000",
        "billerFee": f"{random.uniform(-500, 0):.4f}",
        "billerOUSwitchingFee": f"{random.uniform(-50, 0):.4f}",
        "penaltyFee": "0.0000",
        "clearingTimestamp": clearingTimestamp,
        "paymentChannel": random.choice(["MOB", "WEB", "CARD"]),
        "paymentMode": paymentMode,
        "billerOUCountMonth": "12",
        "billerId": billerId,
        "billerCategory": "Loan Repayment",
        "splitPay": "false",
        "reversal": "false",
        "decline": "false",
        "casProcessed": "true",
        "settlementCycleId": settlementCycleId,
        "customerConvenienceFeeCGST": "0.0000",
        "customerConvenienceFeeIGST": "0.0000",
        "customerConvenienceFeeSUTGST": "0.0000",
        "billerFeeCGST": "0.0000",
        "billerFeeIGST": f"{random.uniform(-90, 0):.4f}",
        "billerFeeSUTGST": "0.0000",
        "billerOUSwitchingFeeCGST": f"{random.uniform(-5, 0):.4f}",
        "billerOUSwitchingFeeIGST": "0.0000",
        "billerOUSwitchingFeeSUTGST": f"{random.uniform(-5, 0):.4f}",
        "penaltyFeeCGST": "0.0000",
        "penaltyFeeIGST": "0.0000",
        "penaltyFeeSUTGST": "0.0000",
        "offUsPay": "true",
        "remarks": "NA"
    }

    csv_data_billconn = None
    csv_data_vtbt = None

    if flag!="REFUND" :
        #refund aanel row skip, failure txn amt radnom, succ same amt
        trnReqDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        if int(txnAmount) == 0:
            trnAmt = random.randint(1000, 1000000)
        else :
            trnAmt = int(txnAmount)
        
        NPCICOMPLIANCEDESC = {
            1000: ["Technical Error Occured"],
            1005: ["BOU Received Failure Ack from NPCI For Response"],
            1010: ["Request Validation success. Success Ack Sent"],
            1011: ["Invalid Request"],
            1020: ["Connection Refused"],
            2010: ["Fetch Request Sent to Biller"],
            2110: ["Failure Fetch Response Received From Biller"],
            2120: ["Success Fetch Response Received From Biller"],
            2130: ["Txn Status is Failure at NPCI"],
            2140: ["Txn Status is Success at NPCI"],
            2150: ["Success Validation Response Received From Biller"],
            2160: ["Failure Validation Response Received From Biller"],
            2220: [
                "Success Pay Response Received From Biller",
                "Success Response Received From BOU",
                "Success Response Received From NPCI"
            ],
            2230: ["Failure Pay Response Received From Biller"],
            2222: ["Deemed Success Sent to NPCI, Waiting for Biller response"],
            5000: ["Request Received From Agent"],
            5002: ["On-US Request Received From COU"],
            5010: ["Request Sent to NPCI"],
            5015: ["NPCI Rejected The Request"],
            5020: ["Response Not Received"],
            5040: [
                "Failure Response Received From BOU",
                "Failure Response Received From NPCI"
            ],
            5050: ["Transaction Reversed"],
            7000: ["OTP Validation Passed"],
            7010: ["OTP Validation Failed"],
            8001: ["Remitter Name info not sent"],
            8002: ["Remitter Name info not in required format"],
            8003: ["Payment Ref ID not sent"],
            8004: ["Payment Ref ID not in required format"],
            8005: ["Payment Mode info not sent"],
            8006: ["Internet Banking info not sent"],
            8007: ["Internet Banking info not in required format"],
            8009: ["Debit Card info not in required format"],
            8010: ["Prepaid Card info not sent"],
            8011: ["Prepaid Card info not in required format"],
            8012: ["IMPS info not sent"],
            8013: ["IMPS info not in required format"],
            8014: ["NEFT info not sent"],
            8015: ["NEFT info not in required format"],
            8016: ["UPI info not sent"],
            8017: ["UPI info not in required format"],
            8018: ["Wallet info not sent"],
            8019: ["Wallet info not in required format"],
            8020: ["AEPS info not sent"],
            8021: ["AEPS info not in required format"],
            8022: ["Account Transfer info not sent"],
            8023: ["Account Transfer info not in required format"],
            8024: ["Bharat QR info not sent"],
            8025: ["Bharat QR info not in required format"],
            8026: ["Bhim Aadhaar Pay info not sent"],
            8027: ["Bhim Aadhaar Pay info not in required format"],
            8028: ["Payment Account Info not sent"]
        }

        success_codes = [
            1010,
            2010,
            2120,
            2140,
            2150,
            2220,
            5000,
            5010,
            2220,
            5002,
            7000,
            2220
            
        ]

        failure_codes = [
            8001, 8002, 8003, 8004, 8005, 8006, 8007, 8009,
            8010, 8011, 8012, 8013, 8014, 8015, 8016, 8017,
            8018, 8019, 8020, 8021, 8022, 8023, 8024, 8025,
            8026, 8027, 8028, 5040, 7010, 5050, 5040, 1011,
            1000, 2110, 1020, 2130, 2160, 2230, 1005, 5015,
            5020, 2222
        ]

        
        c1 = ["yes", "other"]
        weights = [0.7, 0.3]

        choice = random.choices(c1, weights=weights, k=1)[0]

        if choice == "yes":
            currStatusCode = random.choice([2220, 2220, 2220, 2220, 2220, 2220, 2222, 2140, 2230, 8027, 8028])
        else:
            currStatusCode = random.choice(success_codes + failure_codes)

        global BOUTRNREFNO

        csv_data_vtbt = {
            "BOUTRNREFNO" : BOUTRNREFNO, 
            "LVID" : 51, 
            "NPCIREFNO" : "", 
            "BILLERID" : 123456, 
            "TRNREQDATE" : trnReqDate, #ivide timestamp
            "TRNAMT" : trnAmt, 
            "AUTH1" : "", 
            "AUTH2" : "", 
            "AUTH3" : "", 
            "AUTH4" : "", 
            "AUTH5" : "", 
            "AUTH6" : "",
            "AUTH7" : "",
            "CURRSTATUSCODE" : currStatusCode, #random codes from status files
            "CURRSTATUSDESC" : "", 
            "TXNREFERENCEID" : txnReferenceId, 
            "MSGTPEID" : "", 
            "ONUSFLAG" : "", 
            "BILLAMOUNT" : "", 
            "BILLDATE" : "", 
            "BILLDUEDATE" : "", 
            "BILLID" : "", 
            "BILLNUMBER" : "", 
            "CARDNUMBER" : "", 
            "CARDTYPE" : "", 
            "PARTIALPAYMENT" : "", 
            "PAYMENTAMOUNT" : "", 
            "PAYMENTID" : "",
            "PAYMENTSTATUS" : "", 
            "PAYMENTTYPE" : "", 
            "PAYWITHOUTBILL" : "", 
            "NPCIBILLERID" : billerId,
            "TRACEID" : "", 
            "SOURCEID" : "", 
            "NPCIBOUINREFNO" : "", 
            "BILLERTXNID"  : "", 
            "ISADHOC" : "", 
            "BDSBILLERID" : "", 
            "AGNTID" : "", 
            "MSGID" : "", 
            "PAYREF1" : "", 
            "PAYREF2" : "", 
            "PAYREF3" : "",
            "CUSTEMAIL" : "", 
            "CUSTMOBILE" : "267C893B1E24E5BF35C14253FFBBE595", 
            "ORGSTATUSCODE" : "",
            "NPCIAGNTID" : "",
            "PAYMENTMODE" : paymentMode, #same payment mode as transactions
            "RETRYCOUNT" : -1,
            "OFFUSFLAG" : "", 
            "COUCUSTCONVFEE" : "", 
            "NPCISTATUSCODE" : "", 
            "NPCISTATUSDESC" : "", 
            "NPCICOMPLIANCECODE" : "",
            "NPCICOMPLIANCEDESC" : NPCICOMPLIANCEDESC[currStatusCode][0],     #currstatuscoe corresponding desc kooduthalum 2220 etom kooduthal, 2222, 2140, 2230, 8 starting
            "SITXN": "", 
            "ORIGREFID": "",
            "OUID": "HD51",
            "BILLERCONNECTSTATUS" : "",
            "PAYMENTREFID" : "", 
            "RECEIVEDAUTH": "",
            "REMITTERNAME" : "", 
            "DIRECTBILLCONTENTID" : "",
            "DIRECTBILLCHANNEL" : "",
            "UPDATED_ON" : "",
            "ISRECONPROCESSED" : "N",
            "ISRECONCONSIDERED" : "N"
        }

        c2 = ["SUCCESS", "other"]
        weights = [0.7, 0.3]
        choice2 = random.choices(c2, weights=weights, k=1)[0]
        if choice2 == "SUCCESS":
            csvStatus = "SUCCESS"
        else:
            csvStatus = random.choice(["PENDING", "FAILURE"])

        postingDate = (datetime.now(timezone(timedelta(hours=5, minutes=30)))).strftime("%Y-%m-%d %H:%M:%S")

        if flag=="SUCCESS":
            billAmount = str(txnAmount)
        else:
            billAmount = str(trnAmt)

        csv_data_billconn = {
            "BC_MASTER_ID" : BOUTRNREFNO,
            "OBJECT_ID" : "A23456",
            "SOURCE_ID" : "A23456",
            "BILLER_ID" : billerId,
            "VALID_UNTIL" : postingDate,
            "VALIDATION_ID" : "",
            "BILLER_REFERENCE_NO" : str(BOUTRNREFNO),
            "BILLFETCH_PARAMS" : "",
            "PAYMENT_ID" : "",
            "SOURCE_REF_NO" : "",
            "BBPS_REF_NO" : txnReferenceId,
            "TXN_DATE_TIME" : "",
            "POSTING_ID" : "",
            "POSTING_DATE" : "2025-06-18 16:33:56.381025",
            "STATUS" : csvStatus,      
            "RETRY_COUNT" : 1,              #to bw changed
            "BILLER_RETRY" : "0",  
            "CREATED_AT" : postingDate,
            "UPDATED_AT" : postingDate,
            "CREATED_BY" : "A23456",
            "UPDATED_BY" : "A23456",
            "BOU_REQ_RESP_ID" : 123456,
            "VALIDATION_DATE" : "",
            "TRACE_ID" : "A23456",          #to be changed
            "BILLER_CONNECT_RETRY" : "0",
            "REQ_BD_TIMESTAMP" : "25-AUG-24 07.30.54.000000000 PM",
            "BILL_DATE" : "",
            "BILL_DUE_DATE" : "",
            "BC_ERROR_CODE" : "",
            "BC_ERROR_MESSAGE" : "",
            "VENDOR_RRN" : "",
            "AUTH1" : "",
            "AUTH2" : "",
            "AUTH3" : "A23456",
            "AUTH4" : "",
            "VENDOR_REF_ID" : "",
            "SUB_DIV_NAME" : "",
            "BILL_AMOUNT" : billAmount, #succ same , fail same as vtbt refund skip 
            "BOU_CONV_FEES" : "0",
            "COU_CONV_FEES" : "0",
            "MODE_OF_PAYMENT" : paymentMode,
            "BILLER_REQUEST_TYPE" : "",
            "OUID" : ""
        }

        BOUTRNREFNO += 1
        
    return transaction, csv_data_vtbt, csv_data_billconn
    

def indent(elem, level=0):
    pad = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = pad + "  "
        for child in elem:
            indent(child, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = pad
    else:
        if not elem.tail or not elem.tail.strip():
            elem.tail = pad

def create_xml(transactions_list, output_file_xml):
    rawfile = ET.Element("RAWFile", ouId="HD51")
    for transaction in transactions_list:
        transactions = ET.SubElement(rawfile, "transactions")
        for key, value in transaction.items():
            ET.SubElement(transactions, key).text = value

    signature = ET.SubElement(rawfile, "Signature", xmlns="http://www.w3.org/2000/09/xmldsig#")
    signed_info = ET.SubElement(signature, "SignedInfo")
    ET.SubElement(signed_info, "CanonicalizationMethod", Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315")
    ET.SubElement(signed_info, "SignatureMethod", Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256")
    reference = ET.SubElement(signed_info, "Reference", URI="")
    transforms = ET.SubElement(reference, "Transforms")
    ET.SubElement(transforms, "Transform", Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature")
    ET.SubElement(reference, "DigestMethod", Algorithm="http://www.w3.org/2001/04/xmlenc#sha256")
    ET.SubElement(reference, "DigestValue").text = "x1eQX0UhXo3I2297x2LUIrC5ufElD4eWviOa4W+ahdA="
    ET.SubElement(signature, "SignatureValue").text = "SEP/Z813RbxhHg3MGGQAm/BxGw9gBrgXY12I2zk+Pns5MgMtzIwzzM6LAF+BJCj18GWhP5azyz2q"

    indent(rawfile)
    tree = ET.ElementTree(rawfile)
    tree.write(output_file_xml, encoding="UTF-8", xml_declaration=True)

def generate_csv(csv_data_list, output_file_csv):
    if not csv_data_list:
        return
    headers = list(csv_data_list[0].keys())
    with open(output_file_csv, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for row in csv_data_list:
            writer.writerow(row)

def generate_files(countSucc, countRefund, countFailed, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    transactions_list = []
    csv_data_vtbt_list = []
    csv_data_billconn_list = []

    for flag, count in [("SUCCESS", countSucc), ("REFUND", countRefund), ("FAILURE", countFailed)]:
        for _ in range(count):
            txn, csv_vtbt,csv_billconn = generate_random_transaction(flag)
            transactions_list.append(txn)
            if csv_vtbt:
                csv_data_vtbt_list.append(csv_vtbt)
            if csv_billconn:
                csv_data_billconn_list.append(csv_billconn)

    i = 1
    while True:
        output_file_xml = os.path.join(output_dir, f"transactions_{i}.xml")
        if not os.path.exists(output_file_xml):
            break
        i += 1
    i = 1
    while True:
        output_file_csv_vtbt = os.path.join(output_dir, f"transactions_Vtbt_{i}.csv")
        if not os.path.exists(output_file_csv_vtbt):
            break
        i += 1
    i = 1
    while True:
        output_file_csv_billerconn = os.path.join(output_dir, f"transactions_BillerConn_{i}.csv")
        if not os.path.exists(output_file_csv_billerconn):
            break
        i += 1

    create_xml(transactions_list, output_file_xml)
    generate_csv(csv_data_vtbt_list, output_file_csv_vtbt)
    generate_csv(csv_data_billconn_list, output_file_csv_billerconn)



# UI Code :

def select_folder():
    global selected_folder
    folder = filedialog.askdirectory()
    if folder:
        selected_folder = folder
        folder_label.config(text=folder)

def validate_inputs():
    try:
        # s = int(settlement_cycle_id.get())
        n = int(total_transactions.get())
        succ = success_count.get().strip()
        refund = refund_count.get().strip()
        failed = failed_count.get().strip()

        # if s<1 or s>8 :
        #     raise ValueError("The settlement Cycle Id should be in the range 1-8.")
        
        filled = [bool(succ), bool(refund), bool(failed)]
        if filled.count(True) < 2:
            raise ValueError("Please enter at least two of the three transaction counts (Success, Refund, Failed).")

        if not succ:
            refund_val = int(refund)
            failed_val = int(failed)
            succ_val = n - refund_val - failed_val
            if succ_val < 0:
                raise ValueError("Calculated Success count is negative. Please check your inputs.")
        else:
            succ_val = int(succ)

        if not refund:
            succ_val = int(success_count.get())
            failed_val = int(failed) if failed else int(failed_count.get())
            refund_val = n - succ_val - failed_val
            if refund_val < 0:
                raise ValueError("Calculated Refund count is negative. Please check your inputs.")
        else:
            refund_val = int(refund)

        if not failed:
            succ_val = int(success_count.get())
            refund_val = int(refund_count.get())
            failed_val = n - succ_val - refund_val
            if failed_val < 0:
                raise ValueError("Calculated Failed count is negative. Please check your inputs.")
        else:
            failed_val = int(failed)

        if succ_val < 0 or refund_val < 0 or failed_val < 0:
            raise ValueError("Transaction counts cannot be negative.")
        if succ_val + refund_val + failed_val != n:
            raise ValueError("Sum of Success, Refund, and Failed must equal Total Transactions.")
        if refund_val > succ_val:
            raise ValueError("Success transactions should be more than Refund transactions.")
        if not selected_folder:
            raise ValueError("Please select an output folder.")

        return succ_val, refund_val, failed_val
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
        return None

def display_count():
    validated = validate_inputs()
    if not validated:
        return
    _, succ_val, refund_val, failed_val = validated
    messagebox.showinfo(
        "Transaction Counts",
        f"Success: {succ_val}\nRefund: {refund_val}\nFailed: {failed_val}"
    )

def generate_transactions():
    global s
    s = str(settlement_cycle_id.get())

    global BOUTRNREFNO
    BOUTRNREFNO = int(BOUTRNREFNO_starting_no.get())

    global BillerId
    BillerId = str(BillerId.get())

    validated = validate_inputs()
    if not validated:
        return
    succ_val, refund_val, failed_val = validated
    try:
        generate_files(succ_val, refund_val, failed_val, selected_folder)
        messagebox.showinfo("Success", "Transactions generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate transactions:\n{e}")

root = tk.Tk()
root.title("Transaction Data Generator")

tk.Label(root, text="Settlement Cycle ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
settlement_cycle_id = tk.Entry(root)
settlement_cycle_id.grid(row=0, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="BOUTRNREFNO starting number :").grid(row=1, column=0, padx=10, pady=5, sticky="e")
BOUTRNREFNO_starting_no = tk.Entry(root)
BOUTRNREFNO_starting_no.grid(row=1, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Biller Id :").grid(row=2, column=0, padx=10, pady=5, sticky="e")
BillerId = tk.Entry(root)
BillerId.grid(row=2, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Total Transactions:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
total_transactions = tk.Entry(root)
total_transactions.grid(row=3, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Number of SUCCESS Transactions:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
success_count = tk.Entry(root)
success_count.grid(row=4, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Number of REFUND Transactions:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
refund_count = tk.Entry(root)
refund_count.grid(row=5, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Number of FAILED Transactions:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
failed_count = tk.Entry(root)
failed_count.grid(row=6, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Biller OUID : ").grid(row=7, column=0, padx=10, pady=5, sticky="e")
BillerOuid = tk.Entry(root)
BillerOuid.grid(row=7, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Output Folder:").grid(row=8, column=0, padx=10, pady=5, sticky="e")
folder_label = tk.Label(root, text="Select Folder", anchor="w", width=30)
folder_label.grid(row=8, column=1, padx=10, pady=5, sticky="w")
tk.Button(root, text="Select Folder", command=select_folder).grid(row=8, column=2, padx=10, pady=5)

tk.Button(root, text="Generate", command=generate_transactions).grid(row=9, column=0, columnspan=2, pady=10)
tk.Button(root, text="Display Count", command=display_count).grid(row=9, column=2, pady=10)

root.mainloop()

