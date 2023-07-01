from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_table import Table, Col, LinkCol
from datetime import datetime
import os
from ocr import OCR
from receipt_db import Receipt, ReceiptDB

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db = ReceiptDB('receipts.db')
db.create_table()

class ReceiptTable(Table):
    id = Col('Receipt ID')
    vendor_name = Col('Vendor Name', allow_sort=True)
    date = Col('Date', allow_sort=True)
    total_amount = Col('Total Amount')
    edit = LinkCol('Edit', 'edit_receipt', url_kwargs=dict(receipt_id='id'), attr = 'id', allow_sort=False, anchor_attrs={'class': 'btn btn-secondary'})
    delete = LinkCol('Delete', 'delete_receipt', url_kwargs=dict(receipt_id='id'), attr='id', allow_sort=False, anchor_attrs={'class': 'btn btn-danger', 'onclick': 'return confirmDelete(\'id\')'})
    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('application', sort=col_key, direction=direction)
    # Add Bootstrap class attributes to table elements
    classes = ['table', 'table-striped', 'table-bordered', 'table-hover']

@app.route('/')
def home():
    return redirect(url_for('application'))

@app.route('/app', methods=['GET', 'POST'])
def application():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded', 400

        file = request.files['file']
        if file.filename == '':
            return 'No file selected', 400

        file_bytes = file.read()  # Read the file content as bytes

        extracted_text = OCR.extract_text_from_bytes(file_bytes)
        total_amount = OCR.extract_total_amount(extracted_text)
        vendor_name = OCR.extract_vendor_name(extracted_text)
        date = OCR.extract_date(extracted_text)

        receipt = Receipt({
            0: None,
            1: vendor_name,
            2: date,
            3: total_amount
        })

        db.insert_receipt(receipt)

        # Clear the form data to prevent resubmission on refresh
        return redirect(request.url)

    receipts = db.get_all_receipts()
    table = ReceiptTable(receipts)  # Pass the receipts list to the table object
    table.border = True  # Optionally, set a border for the table

    return render_template('app.html', table=table)

@app.route('/edit/<int:receipt_id>', methods=['GET', 'POST'])
def edit_receipt(receipt_id):
    if request.method == 'POST':
        vendor_name = request.form.get('vendor_name')
        date = request.form.get('date')
        total_amount = request.form.get('total_amount')

        data = [receipt_id, vendor_name, date, total_amount]
        receipt = Receipt(data)
        
        db.update_receipt(receipt_id, vendor_name, date, total_amount)

        return redirect(url_for('application'))

    receipt = db.get_receipt(receipt_id)
    return render_template('edit.html', receipt=receipt)

@app.route('/delete/<int:receipt_id>', methods=['GET', 'POST'])
def delete_receipt(receipt_id):
    if request.method == 'GET':
        db.delete_receipt(receipt_id)
        return redirect(url_for('application'))

@app.route('/download/table')
def download_table():
    receipts = db.get_all_receipts()
    if not receipts:
        return 'No receipts found', 404

    # Generate the table data as a CSV file
    csv_data = "Receipt ID,Image Path,Vendor Name,Date,Total Amount\n"
    for receipt in receipts:
        csv_data += "{},{},{},{}\n".format(receipt.id, receipt.vendor_name, receipt.date, receipt.total_amount)

    # Create the response with the CSV data
    response = make_response(csv_data)
    response.headers["Content-Disposition"] = "attachment; filename=receipts.csv"
    response.headers["Content-type"] = "text/csv"

    return response

if __name__ == '__main__':
    app.run(port=5001, debug=True)