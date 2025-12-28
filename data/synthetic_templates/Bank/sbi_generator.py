"""
SBI Bank Statement Generator
Generates synthetic bank statements matching the provided SBI format
"""

import os
import random
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.pdfgen import canvas

# Configuration
OUTPUT_DIR = "../../../data/raw_pdfs/SBI"
TRANSACTIONS_CONFIG = [
    (300, 10),  # 10 PDFs with 300 transactions each
    (150, 10),  # 10 PDFs with 150 transactions each
]

# Indian names for realistic accounts
FIRST_NAMES = [
    "RAJESH", "PRIYA", "AMIT", "SNEHA", "VIKRAM", "ANJALI", "SURESH", "DEEPIKA",
    "KARTHIK", "MEERA", "ARUN", "DIVYA", "RAMESH", "KAVITA", "MANOJ", "POOJA",
    "SACHIN", "NISHA", "RAVI", "SWATI", "GOPAL", "REKHA", "VENKAT", "SUNITA"
]

LAST_NAMES = [
    "SHARMA", "KUMAR", "SINGH", "REDDY", "PATEL", "NAIR", "RAO", "GUPTA",
    "VERMA", "KRISHNAN", "IYER", "MEHTA", "DESAI", "JOSHI", "AGARWAL", "MENON",
    "PILLAI", "NAIDU", "CHOWDARY", "BHAT", "CHOUDHARY", "MALHOTRA"
]

# Realistic transaction descriptions
TRANSACTIONS = {
    'food': [
        'UPI-SWIGGY-', 'UPI-ZOMATO-', 'UPI-DOMINOS PIZZA-', 'UPI-MCDONALDS-',
        'UPI-KFC-', 'UPI-SUBWAY-', 'UPI-CAFE COFFEE DAY-', 'UPI-STARBUCKS-',
        'POS PURCHASE-HOTEL ', 'POS PURCHASE-RESTAURANT ', 'UPI-BARBEQUE NATION-'
    ],
    'groceries': [
        'POS PURCHASE-DMART-', 'POS PURCHASE-RELIANCE FRESH-', 'POS PURCHASE-MORE MEGASTORE-',
        'POS PURCHASE-BIG BAZAAR-', 'UPI-BIGBASKET-', 'UPI-GROFERS-', 'POS PURCHASE-SPENCERS-'
    ],
    'travel': [
        'UPI-UBER INDIA-', 'UPI-OLA CABS-', 'UPI-RAPIDO-', 'POS PURCHASE-INDIAN OIL-',
        'POS PURCHASE-HP PETROL-', 'POS PURCHASE-BHARAT PETROLEUM-', 'IMPS-PAYTM-FASTAG',
        'UPI-IRCTC-', 'POS PURCHASE-RAILWAY TICKET-'
    ],
    'shopping': [
        'UPI-AMAZON PAY-', 'UPI-FLIPKART-', 'UPI-MYNTRA-', 'POS PURCHASE-SHOPPERS STOP-',
        'POS PURCHASE-WESTSIDE-', 'POS PURCHASE-PANTALOONS-', 'UPI-AJIO-',
        'POS PURCHASE-LIFESTYLE-', 'UPI-MEESHO-'
    ],
    'entertainment': [
        'UPI-NETFLIX-', 'UPI-AMAZON PRIME-', 'UPI-HOTSTAR-', 'UPI-SPOTIFY-',
        'POS PURCHASE-PVR CINEMAS-', 'POS PURCHASE-INOX-', 'UPI-BOOKMYSHOW-',
        'UPI-SONYLIV-', 'UPI-ZEE5-'
    ],
    'utilities': [
        'BILL PAYMENT-ELECTRICITY BILL', 'UPI-JIO RECHARGE-', 'UPI-AIRTEL RECHARGE-',
        'UPI-VI RECHARGE-', 'BILL PAYMENT-WATER BILL', 'UPI-TATA SKY-',
        'BILL PAYMENT-GAS BILL', 'UPI-ACT FIBERNET-', 'UPI-AIRTEL FIBER-'
    ],
    'atm': [
        'ATM WDL\nATM CASH ', 'ATM WDL\nATM CASH ', 'ATM WDL\nATM CASH '
    ],
    'transfer': [
        'NEFT-', 'IMPS-', 'UPI-', 'RTGS-'
    ],
    'credits': [
        'SALARY CREDIT-', 'NEFT CR-', 'IMPS CR-', 'UPI CR-', 'CREDIT INTEREST'
    ]
}

# Transaction amount ranges (in INR)
AMOUNT_RANGES = {
    'food': (50, 1500),
    'groceries': (200, 5000),
    'travel': (30, 2000),
    'shopping': (300, 15000),
    'entertainment': (99, 999),
    'utilities': (200, 3000),
    'atm': (500, 10000),
    'transfer': (1000, 50000),
    'salary': (25000, 150000),
    'small_credit': (500, 5000),
    'interest': (50, 500)
}


def generate_account_number():
    """Generate a realistic SBI account number"""
    return f"{random.randint(10000000, 99999999)}{random.randint(10000, 99999)}"


def generate_ifsc():
    """Generate realistic IFSC code"""
    branch_code = random.randint(1000, 9999)
    return f"SBIN000{branch_code}"


def generate_micr():
    """Generate realistic MICR code"""
    return f"5{random.randint(10000, 99999)}{random.randint(100, 999)}"


def generate_customer_name():
    """Generate realistic Indian customer names"""
    title1 = random.choice(["Mr.", "Mrs.", "Ms."])
    title2 = random.choice(["Mr.", "Mrs.", "Ms."])
    name1 = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    name2 = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    
    # Sometimes single account holder
    if random.random() < 0.3:
        return f"{title1} {name1}"
    return f"{title1} {name1},{title2} {name2}"


def generate_branch_name():
    """Generate realistic branch names"""
    cities = [
        "MUMBAI MAIN", "DELHI CONNAUGHT PLACE", "BANGALORE KORAMANGALA",
        "CHENNAI ANNA NAGAR", "HYDERABAD BANJARA HILLS", "PUNE SHIVAJI NAGAR",
        "KOLKATA PARK STREET", "AHMEDABAD NAVRANGPURA", "JAIPUR MI ROAD",
        "LUCKNOW HAZRATGANJ", "INDORE VIJAY NAGAR", "KOCHI MG ROAD",
        "CHANDIGARH SECTOR 17", "NAGPUR SITABULDI", "VADODARA ALKAPURI"
    ]
    return random.choice(cities)


def generate_address():
    """Generate realistic Indian addresses"""
    door_no = f"{random.randint(1, 99)}-{random.randint(1, 99)}-{random.randint(1, 999)}"
    streets = ["MAIN ROAD", "GANDHI ROAD", "NEHRU STREET", "MG ROAD", "ANNA SALAI", "BRIGADE ROAD"]
    areas = ["SECTOR " + str(random.randint(1, 50)), "COLONY", "NAGAR", "EXTENSION"]
    pincode = random.randint(110001, 855999)
    
    return f"DNO: {door_no}\n{random.choice(streets)}, {random.choice(areas)}\n{pincode}"


def generate_transaction_date(start_date, end_date):
    """Generate random date within range"""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


def generate_transactions(num_transactions, start_date, end_date, opening_balance):
    """Generate realistic transactions with proper balance logic"""
    transactions = []
    current_balance = opening_balance
    
    # Determine salary day (usually 1st or last day of month)
    salary_day = random.choice([1, 28, 29, 30])
    salary_amount = random.randint(*AMOUNT_RANGES['salary'])
    
    # Generate dates first
    dates = sorted([generate_transaction_date(start_date, end_date) for _ in range(num_transactions)])
    
    for i, trans_date in enumerate(dates):
        # Add salary credit on salary day
        if trans_date.day == salary_day and random.random() < 0.8:
            transactions.append({
                'date': trans_date,
                'narration': f"SALARY CREDIT-COMPANY NAME",
                'ref': str(random.randint(100000, 999999)),
                'debit': 0,
                'credit': salary_amount,
                'balance': current_balance + salary_amount
            })
            current_balance += salary_amount
            continue
        
        # Determine transaction type based on realistic distribution
        rand = random.random()
        if rand < 0.25:  # 25% food
            category = 'food'
            trans_type = random.choice(TRANSACTIONS['food'])
            amount = random.randint(*AMOUNT_RANGES['food'])
            narration = trans_type + str(random.randint(1000, 9999))
            debit = amount
            credit = 0
        elif rand < 0.40:  # 15% groceries
            category = 'groceries'
            trans_type = random.choice(TRANSACTIONS['groceries'])
            amount = random.randint(*AMOUNT_RANGES['groceries'])
            narration = trans_type + str(random.randint(1000, 9999))
            debit = amount
            credit = 0
        elif rand < 0.55:  # 15% travel
            category = 'travel'
            trans_type = random.choice(TRANSACTIONS['travel'])
            amount = random.randint(*AMOUNT_RANGES['travel'])
            narration = trans_type + str(random.randint(1000, 9999))
            debit = amount
            credit = 0
        elif rand < 0.68:  # 13% shopping
            category = 'shopping'
            trans_type = random.choice(TRANSACTIONS['shopping'])
            amount = random.randint(*AMOUNT_RANGES['shopping'])
            narration = trans_type + str(random.randint(1000, 9999))
            debit = amount
            credit = 0
        elif rand < 0.76:  # 8% entertainment
            category = 'entertainment'
            trans_type = random.choice(TRANSACTIONS['entertainment'])
            amount = random.randint(*AMOUNT_RANGES['entertainment'])
            narration = trans_type + str(random.randint(1000, 9999))
            debit = amount
            credit = 0
        elif rand < 0.83:  # 7% utilities
            category = 'utilities'
            trans_type = random.choice(TRANSACTIONS['utilities'])
            amount = random.randint(*AMOUNT_RANGES['utilities'])
            narration = trans_type
            debit = amount
            credit = 0
        elif rand < 0.90:  # 7% ATM
            trans_type = random.choice(TRANSACTIONS['atm'])
            amount = random.randint(*AMOUNT_RANGES['atm'])
            atm_id = random.randint(1000, 9999)
            narration = f"{trans_type}{atm_id} {generate_branch_name()}"
            debit = amount
            credit = 0
        elif rand < 0.95:  # 5% transfers
            trans_type = random.choice(TRANSACTIONS['transfer'])
            amount = random.randint(*AMOUNT_RANGES['transfer'])
            narration = trans_type + f"{random.choice(FIRST_NAMES)}-{random.randint(1000, 9999)}"
            debit = amount
            credit = 0
        else:  # 5% credits
            credit_type = random.choice(TRANSACTIONS['credits'])
            if 'INTEREST' in credit_type:
                amount = random.randint(*AMOUNT_RANGES['interest'])
                narration = credit_type
            else:
                amount = random.randint(*AMOUNT_RANGES['small_credit'])
                narration = credit_type + f"{random.choice(FIRST_NAMES)}"
            debit = 0
            credit = amount
        
        # Update balance
        if debit > 0:
            new_balance = current_balance - debit
        else:
            new_balance = current_balance + credit
        
        # Avoid negative balance
        if new_balance < 0:
            # Add a credit transaction to balance
            emergency_credit = abs(new_balance) + random.randint(5000, 20000)
            transactions.append({
                'date': trans_date,
                'narration': f"NEFT CR-{random.choice(FIRST_NAMES)}",
                'ref': str(random.randint(100000, 999999)),
                'debit': 0,
                'credit': emergency_credit,
                'balance': current_balance + emergency_credit
            })
            current_balance += emergency_credit
            new_balance = current_balance - debit
        
        transactions.append({
            'date': trans_date,
            'narration': narration,
            'ref': str(random.randint(1000, 999999)),
            'debit': debit,
            'credit': credit,
            'balance': new_balance
        })
        
        current_balance = new_balance
    
    return transactions


def create_header_footer(canvas, doc):
    """Add header and footer to each page"""
    canvas.saveState()
    
    # Header - Bank name
    canvas.setFont('Helvetica-Bold', 14)
    canvas.drawString(30*mm, 280*mm, "State Bank of India")
    
    # Footer
    canvas.setFont('Helvetica', 8)
    canvas.drawString(30*mm, 15*mm, "**This is a computer generated statement and does not require a signature")
    canvas.drawRightString(180*mm, 15*mm, "https://retail.onlinesbi.com/retail/printstatement.htm")
    canvas.drawCentredString(105*mm, 10*mm, f"Page {doc.page}")
    
    canvas.restoreState()


def generate_pdf(filename, num_transactions):
    """Generate a single PDF bank statement"""
    
    # Generate random account details
    account_number = generate_account_number()
    customer_name = generate_customer_name()
    branch = generate_branch_name()
    address = generate_address()
    ifsc = generate_ifsc()
    micr = generate_micr()
    
    # Generate statement period (last 30 days)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Generate opening balance
    opening_balance = random.randint(10000, 200000)
    
    # Generate transactions
    transactions = generate_transactions(num_transactions, start_date, end_date, opening_balance)
    
    # Create PDF
    pdf_path = os.path.join(OUTPUT_DIR, filename)
    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                           leftMargin=30*mm, rightMargin=30*mm,
                           topMargin=35*mm, bottomMargin=25*mm)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=10,
        textColor=colors.black,
        spaceAfter=2,
        alignment=TA_LEFT
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        alignment=TA_LEFT
    )
    
    # Account details section
    account_info = [
        ['Account Number', account_number, 'Branch', branch],
        ['Address', Paragraph(address.replace('\n', '<br/>'), normal_style), 'Account Type', 'SBCHQ-SGSP-PUB IND -SILVER-INR'],
        ['Account Name', Paragraph(customer_name, normal_style), 'Interest Rate(% p.a.)', '3.25'],
        ['CIF No.', str(random.randint(10000000000, 99999999999)), 'IFS Code', ifsc],
        ['Nomination Registered', 'No', 'MICR Code', micr],
        ['Balance as on', f"{start_date.strftime('%d/%m/%Y')}", f"{opening_balance:,.2f}", '']
    ]
    
    account_table = Table(account_info, colWidths=[40*mm, 45*mm, 40*mm, 45*mm])
    account_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.Color(0.95, 0.95, 0.95)),
        ('BACKGROUND', (2, 0), (2, -1), colors.Color(0.95, 0.95, 0.95)),
    ]))
    
    story.append(account_table)
    story.append(Spacer(1, 5*mm))
    
    # Statement period
    period_text = Paragraph(
        f"<b>Account Statement for the period {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}</b>",
        header_style
    )
    story.append(period_text)
    story.append(Spacer(1, 3*mm))
    
    # Transaction table header
    trans_data = [['Date (Value Date)', 'Narration', 'Ref/Cheque No.', 'Debit', 'Credit', 'Balance']]
    
    # Add transactions
    for trans in transactions:
        date_str = f"{trans['date'].strftime('%d-%b-%y')}\n({trans['date'].strftime('%d-%b-%Y')})"
        debit_str = f"{trans['debit']:,.2f}" if trans['debit'] > 0 else ""
        credit_str = f"{trans['credit']:,.2f}" if trans['credit'] > 0 else ""
        balance_str = f"{trans['balance']:,.2f}"
        
        trans_data.append([
            date_str,
            trans['narration'],
            trans['ref'],
            debit_str,
            credit_str,
            balance_str
        ])
    
    # Create transaction table
    trans_table = Table(trans_data, colWidths=[28*mm, 50*mm, 25*mm, 22*mm, 22*mm, 23*mm])
    trans_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (2, -1), 'LEFT'),
        ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9)),
    ]))
    
    story.append(trans_table)
    
    # Build PDF
    doc.build(story, onFirstPage=create_header_footer, onLaterPages=create_header_footer)
    print(f"Generated: {filename}")


def main():
    """Main function to generate all PDFs"""
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Starting SBI Bank Statement Generation...")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 60)
    
    pdf_counter = 1
    
    for num_trans, num_pdfs in TRANSACTIONS_CONFIG:
        print(f"\nGenerating {num_pdfs} PDFs with {num_trans} transactions each...")
        
        for i in range(num_pdfs):
            filename = f"SBI_Statement_{pdf_counter:02d}_{num_trans}txn.pdf"
            generate_pdf(filename, num_trans)
            pdf_counter += 1
    
    print("\n" + "=" * 60)
    print(f"✓ Successfully generated {pdf_counter - 1} SBI bank statement PDFs")
    print(f"✓ Location: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()