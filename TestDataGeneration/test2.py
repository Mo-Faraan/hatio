import xml.etree.ElementTree as ET
import random
from datetime import datetime, timedelta, date, timezone
import os
import string
import csv
import tkinter as tk
from tkinter import messagebox, filedialog

selected_folder = ""
successTxnRefIds = dict()
s=1

def generate_random_transaction(flag):
    txnDate = date.today().strftime("%Y-%m-%d")
    clearingTimestamp = (datetime.now(timezone(timedelta(hours=5, minutes=30)))).strftime("%Y-%m-%dT%H:%M:%S+05:30")

    characters = string.ascii_uppercase + string.digits
    msgId = random.choice(string.ascii_uppercase) + "".join(random.choices(characters, k=33))
    txnReferenceId = random.choice(string.ascii_uppercase) + "".join(random.choices(characters, k=19))

    settlementCycleId = "00"+str(s)+txnDate.replace("-","")+"00"

    billerIds = ["HDFC00000NATW1", "MPPK00000MAP01", "HDFC00000NAT5K", "UTTA00000UTT7M", "MPEZ00000MAP02", "HATHWAY00NAT01", "HDBF00000NATGJ", "TATAPWR00DEL01", "NESCO0000ODI01", "AYEF00000NATZB", "MPCZ00000MAP01", "SOLA00000MAHG9", "MADH00000GUJOY", "ELEC00000CHA3L", "INDI00000NAT26", "MUNI00000CHANI", "LUCK00000LUC9J", "WESCO0000ODI01", "CNHI00000NATNZ", "PATN00000BIHJ3", "FUSI00000DEL5E", "ARTH00000NAT4D", "COMM00000TELQ2", "HUKK00000NATGM"]
    billerId = random.choice(billerIds)
    
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
        "paymentMode": random.choice(["Internet Banking", "Credit Card", "UPI"]),
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

    #refund aanel row skip, failure txn amt radnom, succ same amt
    csv_data = {
        "BOUTRNREFNO" : 100000, 
        "LVID" : 51, 
        "NPCIREFNO" : "", 
        "BILLERID" : 123456, 
        "TRNREQDATE" : date.today(), #timestamp
        "TRNAMT" : txnAmount, 
        "AUTH1" : "", 
        "AUTH2" : "", 
        "AUTH3" : "", 
        "AUTH4" : "", 
        "AUTH5" : "", 
        "AUTH6" : "",
        "AUTH7" : "",
        "CURRSTATUSCODE" : int(responseCode), #random codes from status files
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
        "NPCIBILLERID" : billerId, //
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
        "PAYMENTMODE" : "Credit Card", //same payment mode as transactions
        "RETRYCOUNT" : -1,
        "OFFUSFLAG" : "", 
        "COUCUSTCONVFEE" : "", 
        "NPCISTATUSCODE" : "", 
        "NPCISTATUSDESC" : "", 
        "NPCICOMPLIANCECODE" : "",
        "NPCICOMPLIANCEDESC" : mti,     #currstatuscoe corresponding desc kooduthalum 2220 etom kooduthal, 2222, 2140, 2230, 8 starting
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

    return transaction, csv_data
    

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
    csv_data_list = []

    for _ in range(countSucc):
        txn, csvData = generate_random_transaction("SUCCESS")
        transactions_list.append(txn)
        csv_data_list.append(csvData)
    for _ in range(countRefund):
        txn, csvData = generate_random_transaction("REFUND")
        transactions_list.append(txn)
        csv_data_list.append(csvData)
    for _ in range(countFailed):
        txn, csvData = generate_random_transaction("FAILED")
        transactions_list.append(txn)
        csv_data_list.append(csvData)

    i = 1
    while True:
        output_file_xml = os.path.join(output_dir, f"transactions_{i}.xml")
        if not os.path.exists(output_file_xml):
            break
        i += 1
    i = 1
    while True:
        output_file_csv = os.path.join(output_dir, f"transactions_{i}.csv")
        if not os.path.exists(output_file_csv):
            break
        i += 1

    create_xml(transactions_list, output_file_xml)
    generate_csv(csv_data_list, output_file_csv)



# UI Code :

def select_folder():
    global selected_folder
    folder = filedialog.askdirectory()
    if folder:
        selected_folder = folder
        folder_label.config(text=folder)

def validate_inputs():
    try:
        s = int(settlement_cycle_id.get())
        n = int(total_transactions.get())
        succ = success_count.get().strip()
        refund = refund_count.get().strip()
        failed = failed_count.get().strip()

        if s<1 or s>8 :
            raise ValueError("The settlement Cycle Id should be in the range 1-8.")
        
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

        return s, succ_val, refund_val, failed_val
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
    validated = validate_inputs()
    if not validated:
        return
    s, succ_val, refund_val, failed_val = validated
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

tk.Label(root, text="Total Transactions:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
total_transactions = tk.Entry(root)
total_transactions.grid(row=1, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Number of SUCCESS Transactions:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
success_count = tk.Entry(root)
success_count.grid(row=2, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Number of REFUND Transactions:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
refund_count = tk.Entry(root)
refund_count.grid(row=3, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Number of FAILED Transactions:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
failed_count = tk.Entry(root)
failed_count.grid(row=4, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Output Folder:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
folder_label = tk.Label(root, text="Select Folder", anchor="w", width=30)
folder_label.grid(row=5, column=1, padx=10, pady=5, sticky="w")
tk.Button(root, text="Select Folder", command=select_folder).grid(row=5, column=2, padx=10, pady=5)

tk.Button(root, text="Generate", command=generate_transactions).grid(row=6, column=0, columnspan=2, pady=10)
tk.Button(root, text="Display Count", command=display_count).grid(row=6, column=2, pady=10)

root.mainloop()



csv_data2 = {
    "BC_MASTER_ID" : 123456,
	"OBJECT_ID" : 123456,
	"SOURCE_ID" : 123456,
	"BILLER_ID" : billerId,
	"VALID_UNTIL" : "",
	"VALIDATION_ID" : "",
	"BILLER_REFERENCE_NO" : 123456,
	"BILLFETCH_PARAMS" : "",
	"PAYMENT_ID" : "",
	"SOURCE_REF_NO" : "",
	"BBPS_REF_NO" : txnRefId,
	"TXN_DATE_TIME" : "",
	"POSTING_ID" : "",
	"POSTING_DATE" : date.today(),  timestamp
	"STATUS" : "",   succ, fail pending random success more
	"RETRY_COUNT" : 1,  #to bw changed
	"BILLER_RETRY" : 0,
	"CREATED_AT" : timestamp,
	"UPDATED_AT" TIMESTAMP (6) WITH TIME ZONE NOT NULL ENABLE, timestamp
	"CREATED_BY" VARCHAR2(50) NOT NULL ENABLE, 16
	"UPDATED_BY" VARCHAR2(50) NOT NULL ENABLE,16
	"BOU_REQ_RESP_ID" NUMBER NOT NULL ENABLE,16
	"VALIDATION_DATE" DATE,""
	"TRACE_ID" VARCHAR2(50) NOT NULL ENABLE,16 # to be changed
	"BILLER_CONNECT_RETRY" CHAR(1) DEFAULT '0' NOT NULL ENABLE,0
	"REQ_BD_TIMESTAMP" VARCHAR2(50) DEFAULT '0' NOT NULL ENABLE,"25-AUG-24 07.30.54.000000000 PM"
	"BILL_DATE" VARCHAR2(50),""
	"BILL_DUE_DATE" VARCHAR2(50),
	"BC_ERROR_CODE" VARCHAR2(50),
	"BC_ERROR_MESSAGE" VARCHAR2(255),
	"VENDOR_RRN" VARCHAR2(50),
	"AUTH1" VARCHAR2(50),
	"AUTH2" VARCHAR2(255 CHAR),
	"AUTH3" VARCHAR2(255 CHAR),"jshcgdhj"
	"AUTH4" VARCHAR2(255 CHAR),
	"VENDOR_REF_ID" VARCHAR2(50),
	"SUB_DIV_NAME" VARCHAR2(50),
	"BILL_AMOUNT" VARCHAR2(20) DEFAULT '0', succ same , fail same as vtbt refund skip 
	"BOU_CONV_FEES" VARCHAR2(20) DEFAULT '0',0
	"COU_CONV_FEES" VARCHAR2(20) DEFAULT '0',0
	"MODE_OF_PAYMENT" VARCHAR2(50), same as vtbt
	"BILLER_REQUEST_TYPE" CHAR(1),""
	"OUID" VARCHAR2(255 CHAR)""
}