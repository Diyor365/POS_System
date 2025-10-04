# Simple i18n and currency helper for the POS_System
from PyQt5.QtCore import QCoreApplication

# Basic translation dict for Uzbek UI strings (expandable)
TRANSLATIONS = {
    'en': {
    },
    'uz': {
        'Monthly Sales': "Oylik Savdo",
        'Monthly Profit': "Oylik Foyda",
        'Total Products': "Jami Mahsulotlar",
        'Refresh Data': "Ma'lumotlarni yangilash",
        'Low Stock Alert (Products with Qty ≤ Reorder Level)': "Kam zaxira (Qty ≤ Reorder Level)",
        'Add +': "Qo'sh +",
        'Search': "Qidirish",
        'Item': "Mahsulot",
        'Qty': "Soni",
        'Price': "Narxi",
        'Sub Total : ': "Oraliq summa : ",
        'Discount : ': "Chegirma : ",
        'Total Payment : ': "Umumiy summa : ",
        'Paid : ': "To'langan : ",
        'Balance : ': "Qoldiq : ",
        'Pay': "To'lash",
        'Name': "Nomi",
        'Sku': "SKU",
        'Quantity': "Miqdor",
        'Selling': "Sotish narxi",
        'Purchase': "Xarid narxi",
        'Category': "Kategoriya",
        'Reorder level': "Reorder darajasi",
        'Add': "Qo'sh",
        'Cancel': "Bekor qilish",
        'Save': "Saqlash",
        'Start Date:': "Boshlanish sanasi:",
        'End Date:': "Tugash sanasi:",
        'Apply Filter': "Filtrni qo'llash",
        'Clear Filters': "Filtrni tozalash",
        'Previous': "Oldingi",
        'Next': "Keyingi",
        'Go to Page': "Sahifaga o'tish",
        'Go to page:': "Sahifa raqami:",
        'Total Amount:': "Jami summa:",
        'Payment Details': "To'lov tafsilotlari",
        'Close': "Yopish",
    }
}

# Default locale
LOCALE = 'uz'


def t(key: str) -> str:
    """Translate a UI key to the current locale if available."""
    return TRANSLATIONS.get(LOCALE, {}).get(key, key)


def format_sum(value):
    """Format a numeric value as Uzbek som with space thousand separators and no decimals."""
    try:
        v = int(round(float(value)))
    except Exception:
        v = 0
    s = f"{v:,}".replace(',', ' ')
    return f"{s} soʻm"


# Parsing helper (strip formatting)
def parse_sum(formatted: str) -> float:
    """Parse a formatted sum string back to float/int."""
    if formatted is None:
        return 0.0
    s = str(formatted)
    # remove any non-digit characters except dot and minus
    import re
    s = re.sub(r"[^0-9.-]", "", s)
    try:
        return float(s)
    except Exception:
        return 0.0
