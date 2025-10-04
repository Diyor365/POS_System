from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QDateEdit, QDialog, QTextEdit)
import json
from Application.i18n import format_sum

class PaymentDetails(QDialog):
    def __init__(self, payment_data, parent=None):
        super().__init__(parent)
        self.payment_data = payment_data
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Payment Details")
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        
        layout = QVBoxLayout()
        
        # Create details content
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        
        # Parse the payment data JSON
        payment_info = json.loads(self.payment_data)
        
        # Generate details HTML
        details_html = f"""
        <div style='font-family: Arial; width: 100%;'>
            <h2 style='text-align: center;'>Payment Details</h2>
            <p style='text-align: center;'>{payment_info['timestamp']}</p>
            <hr>
            <table width='100%' style='border-collapse: collapse;'>
                <tr>
                    <th style='text-align: left;'>Item</th>
                    <th style='text-align: right;'>Qty</th>
                    <th style='text-align: right;'>Price</th>
                    <th style='text-align: right;'>Subtotal</th>
                </tr>
        """
        
        # Add items
        for item in payment_info['items']:
            details_html += f"""
                <tr>
                    <td>{item['name']}</td>
                    <td style='text-align: right;'>{item['quantity']}</td>
                    <td style='text-align: right;'>{format_sum(item['price'])}</td>
                    <td style='text-align: right;'>{format_sum(item['subtotal'])}</td>
                </tr>
            """
            
        # Add totals
        details_html += f"""
            </table>
            <hr>
            <table width='100%'>
                <tr>
                    <td style='text-align: right;'>Subtotal:</td>
                    <td style='text-align: right; width: 100px;'>{format_sum(payment_info['subtotal'])}</td>
                </tr>
                <tr>
                    <td style='text-align: right;'>Discount:</td>
                    <td style='text-align: right;'>{format_sum(payment_info['discount'])}</td>
                </tr>
                <tr>
                    <td style='text-align: right;'><b>Total:</b></td>
                    <td style='text-align: right;'><b>{format_sum(payment_info['total'])}</b></td>
                </tr>
                <tr>
                    <td style='text-align: right;'>Paid Amount:</td>
                    <td style='text-align: right;'>{format_sum(payment_info['paid_amount'])}</td>
                </tr>
                <tr>
                    <td style='text-align: right;'>Balance:</td>
                    <td style='text-align: right;'>{format_sum(payment_info['balance'])}</td>
                </tr>
            </table>
        </div>
        """
        
        self.details_text.setHtml(details_html)
        layout.addWidget(self.details_text)
        
        # Add close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
