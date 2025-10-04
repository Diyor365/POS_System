from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QDialog, QTextEdit)
from PyQt5.QtCore import QDateTime, Qt, QDate
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog

class ReceiptView(QDialog):
    def __init__(self, payment_data, parent=None):
        super().__init__(parent)
        self.payment_data = payment_data
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Receipt Preview")
        self.setMinimumWidth(400)
        self.setMinimumHeight(600)
        
        layout = QVBoxLayout()
        
        # Create receipt content
        self.receipt_text = QTextEdit()
        self.receipt_text.setReadOnly(True)
        
        # Helper to format currency like: 53 000
        def fmt(n):
            try:
                val = int(round(float(n)))
            except Exception:
                val = 0
            return f"{val:,}".replace(",", " ")

        # Receipt number fallback
        receipt_no = self.payment_data.get('receipt_no') or self.payment_data.get('id') or 0
        receipt_no = str(receipt_no).zfill(6)

        # Date/time
        dt = QDateTime.currentDateTime()
        if isinstance(self.payment_data.get('created_at'), str):
            # try to use provided created_at if present
            try:
                # expect ISO-like input
                dt = QDateTime.fromString(self.payment_data.get('created_at'), Qt.ISODate)
                if not dt.isValid():
                    dt = QDateTime.currentDateTime()
            except Exception:
                dt = QDateTime.currentDateTime()

        date_str = dt.toString('dd-MM-yyyy')
        time_str = dt.toString('HH:mm:ss')

        # Build items rows
        items_html = ''
        for item in self.payment_data.get('items', []):
            name = item.get('name', '')
            qty = int(item.get('quantity', 0))
            price = int(round(float(item.get('price', 0))))
            subtotal = qty * price
            items_html += f"""
                <tr>
                    <td style='text-align:left; padding:4px 0;'>{name}</td>
                    <td style='text-align:right; padding:4px 0;'>{qty}</td>
                    <td style='text-align:right; padding:4px 0;'>{fmt(price)}</td>
                    <td style='text-align:right; padding:4px 0;'>{fmt(subtotal)}</td>
                </tr>
            """

        subtotal_val = int(round(float(self.payment_data.get('subtotal', 0))))
        discount_val = int(round(float(self.payment_data.get('discount', 0))))
        total_val = int(round(float(self.payment_data.get('total', 0))))
        paid_val = int(round(float(self.payment_data.get('paid_amount', 0))))
        balance_val = paid_val - total_val

        receipt_html = f"""
        <div style='font-family: Arial; width: 100%; font-size:12px;'>
            <div style='text-align:center; font-weight:bold; font-size:14px;'>Xo'jalik mollari do'koni</div>
            <div style='text-align:center;'>Nurobod tumani, Saroy mahalla</div>
            <div style='text-align:center;'>Tel: +998 90 123 45 67</div>
            <hr>
            <div style='font-weight:bold;'>Chek tafsilotlari</div>
            <div>To'lov tafsilotlari</div>
            <div>Sana: {date_str} &nbsp; Vaqt: {time_str}</div>
            <br>
            <table width='100%'>
                <tr>
                    <th style='text-align:left;'>Mahsulot nomi</th>
                    <th style='text-align:right;'>Soni</th>
                    <th style='text-align:right;'>Narxi</th>
                    <th style='text-align:right;'>Jami</th>
                </tr>
                {items_html}
            </table>
            <hr>
            <table width='100%'>
                <tr>
                    <td style='text-align:right;'>Oraliq summa:</td>
                    <td style='text-align:right; width:150px;'>{fmt(subtotal_val)}</td>
                </tr>
                <tr>
                    <td style='text-align:right;'>Chegirma:</td>
                    <td style='text-align:right;'>{fmt(discount_val)}</td>
                </tr>
                <tr>
                    <td style='text-align:right; font-weight:bold;'>Umumiy summa:</td>
                    <td style='text-align:right; font-weight:bold;'>{fmt(total_val)}</td>
                </tr>
                <tr>
                    <td style='text-align:right;'>To'langan summa:</td>
                    <td style='text-align:right;'>{fmt(paid_val)}</td>
                </tr>
                <tr>
                    <td style='text-align:right;'>Qoldiq (naqd qaytim):</td>
                    <td style='text-align:right;'>{fmt(balance_val)}</td>
                </tr>
            </table>
            <br>
            <div style='text-align:center;'>Rahmat! Yana keling!</div>
            <div style='text-align:center;'>Chek № {receipt_no}</div>
        </div>
        """

        self.receipt_text.setHtml(receipt_html)
        layout.addWidget(self.receipt_text)
        
        # Add print buttons
        button_layout = QHBoxLayout()
        
        print_button = QPushButton("Print")
        print_button.clicked.connect(self.print_receipt)
        
        preview_button = QPushButton("Print Preview")
        preview_button.clicked.connect(self.print_preview)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        
        button_layout.addWidget(print_button)
        button_layout.addWidget(preview_button)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def print_receipt(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        
        if dialog.exec_() == QDialog.Accepted:
            self.receipt_text.print_(printer)
            
    def print_preview(self):
        printer = QPrinter()
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(lambda p: self.receipt_text.print_(p))
        preview.exec_()
