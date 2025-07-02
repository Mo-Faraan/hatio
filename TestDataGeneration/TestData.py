import xml.etree.ElementTree as ET
import uuid
import random
from datetime import datetime, timedelta, date, timezone
import os
import secrets
from zoneinfo import ZoneInfo
import string
import csv

s=8
successTxnRefIds = dict()


def generate_random_transaction(flag):
    txnDate = date.today().strftime("%Y-%m-%d")
    clearingTimestamp = (datetime.now(timezone(timedelta(hours=5, minutes=30)))).strftime("%Y-%m-%dT%H:%M:%S+05:30")

    characters = string.ascii_uppercase + string.digits
    msgId = "".join(random.choices(characters, k=34))
    txnReferenceId = "".join(random.choices(characters, k=20))

    settlementCycleId = "00"+str(s)+txnDate.replace("-","")+"00"

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
        "billerOUId": random.choice(["HD51", "JK22", "JK33"]),
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
        "billerId": "HDFC00000NATTK",
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
    return transaction
    

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

def create_xml(transactions_list, output_file):
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
    tree.write(output_file, encoding="UTF-8", xml_declaration=True)

def generate_csv(transactions_list, output_dir):
    if not transactions_list:
        return
    headers = ["TXNREFID", "ABC", "DEF", "HIJ", "LMN"]
    rows=[]
    for txn in transactions_list :
        d={}
        d["TXNREFID"] = txn["txnReferenceId"]
        d["ABC"] = txn["msgId"]
        d["DEF"] = txn["customerOUId"]
        d["HIJ"] = txn["billerOUId"]
        d["LMN"] = txn["responseCode"]
        rows.append(d)
    i = 1
    while True:
        output_file = os.path.join(output_dir, f"transactions_{i}.csv")
        if not os.path.exists(output_file):
            break
        i += 1
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def generate_transactions_in_single_file(countSucc, countRefund, countFailed, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    transactions_list = []
    for _ in range(countSucc):
        txn = generate_random_transaction("SUCCESS")
        transactions_list.append(txn)
    for _ in range(countRefund):
        txn = generate_random_transaction("REFUND")
        transactions_list.append(txn)
    for _ in range(countFailed):
        txn = generate_random_transaction("FAILED")
        transactions_list.append(txn)
    i = 1
    while True:
        output_file = os.path.join(output_dir, f"transactions_{i}.xml")
        if not os.path.exists(output_file):
            break
        i += 1
    create_xml(transactions_list, output_file)
    generate_csv(transactions_list, output_dir)






    