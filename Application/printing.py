from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QTextDocument

def print_sku_label(sku: str, printer_name: str = None) -> bool:
    """Print a simple SKU label to the default/system printer or named printer.

    Returns True on success, False on failure.
    """
    try:
        doc = QTextDocument()
        # Simple HTML: large SKU centered
        html = f"""
        <html><body style='font-family: Arial;'><div style='text-align:center; font-size:48pt; font-weight:bold;'>
        {sku}
        </div></body></html>
        """
        doc.setHtml(html)
        printer = QPrinter()
        if printer_name:
            # try to set printer by name (platform dependent)
            printer.setPrinterName(printer_name)
        # silent print
        doc.print_(printer)
        return True
    except Exception as e:
        print("print_sku_label failed:", e)
        return False
