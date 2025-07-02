import tkinter as tk
from tkinter import messagebox, filedialog
import TestData

selected_folder = ""

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
    validated = validate_inputs()
    if not validated:
        return
    s, succ_val, refund_val, failed_val = validated
    try:
        TestData.s = s
        TestData.generate_transactions_in_single_file(succ_val, refund_val, failed_val, selected_folder)
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