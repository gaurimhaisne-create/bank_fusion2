import random
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

# Sample Indian names - 20 unique first names and 20 unique last names
FIRST_NAMES = ['Khushi', 'Rohan', 'Ankit', 'Neha', 'Pooja', 'Rahul', 'Priya', 'Amit', 'Sakshi', 'Vivek',
               'Aarav', 'Diya', 'Arjun', 'Ishita', 'Karan', 'Riya', 'Siddharth', 'Tanvi', 'Varun', 'Shruti']
LAST_NAMES = ['Agrawal', 'Mehta', 'Verma', 'Sharma', 'Patil', 'Kumar', 'Singh', 'Gupta', 'Reddy', 'Iyer',
              'Joshi', 'Nair', 'Desai', 'Rao', 'Malhotra', 'Kapoor', 'Thakur', 'Patel', 'Bose', 'Menon']

# Track used names to ensure uniqueness
USED_NAMES = set()

# BOI Branches
BOI_BRANCHES = ['Talawade Branch', 'MG Road Branch', 'Koramangala Branch', 'Andheri Branch', 'Connaught Place Branch', 
                'Park Street Branch', 'Banjara Hills Branch', 'Jayanagar Branch', 'Vashi Branch', 'Whitefield Branch']

# Cities and areas
CITIES = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Pune', 'Hyderabad', 'Ahmedabad', 'Jaipur', 'Lucknow']
LOCALITIES = ['KA MOHALLA', 'NAGAR', 'COLONY', 'LAYOUT', 'ENCLAVE', 'EXTENSION', 'SECTOR', 'PHASE']

# Expense categories with BOI-style descriptions
EXPENSE_CATEGORIES = {
    'Grocery': ['MEDR/RELIANCE FRS/', 'MEDR/BIG BAZAAR/', 'MEDR/DMART STORE/', 'MEDR/MORE STORES/', 'MEDR/SPENCER RET/'],
    'Fuel': ['MEDR/HPCL PUMP/', 'MEDR/BPCL PETROL/', 'MEDR/INDIAN OIL/', 'MEDR/SHELL FUEL/', 'MEDR/RELIANCE PT/'],
    'Gas Bill': ['MEDR/IND GAS/', 'MEDR/HP GAS/', 'MEDR/BHARAT GAS/', 'MEDR/ADANI GAS/'],
    'Electricity Bill': ['MEDR/MSEDCL/', 'MEDR/BESCOM/', 'MEDR/TPDDL/', 'MEDR/CESC BILL/'],
    'Mobile Recharge': ['MEDR/AIRTEL RCH/', 'MEDR/JIO RECHARGE/', 'MEDR/VODAFONE/', 'MEDR/BSNL RCH/'],
    'Internet Bill': ['MEDR/ACT FIBER/', 'MEDR/AIRTEL NET/', 'MEDR/JIO FIBER/', 'MEDR/HATHWAY/'],
    'Restaurant': ['MEDR/DOMINOS/', 'MEDR/PIZZA HUT/', 'MEDR/KFC REST/', 'MEDR/MCDONALD/', 'MEDR/SUBWAY/'],
    'Swiggy': ['MEDR/SWIGGY/', 'MEDR/SWIGGY ORD/', 'MEDR/SWIGGY DEL/', 'MEDR/SWIGGY FD/'],
    'Zomato': ['MEDR/ZOMATO/', 'MEDR/ZOMATO ORD/', 'MEDR/ZOMATO DEL/', 'MEDR/ZOMATO FD/'],
    'Amazon': ['MEDR/AMAZON IND/', 'MEDR/AMAZON PAY/', 'MEDR/AMAZON SHP/', 'MEDR/AMAZON/'],
    'Flipkart': ['MEDR/FLIPKART/', 'MEDR/FLIPKART SHP/', 'MEDR/FLIPKART PAY/', 'MEDR/FLIPKART IND/'],
    'Medical': ['MEDR/APOLLO HOSP/', 'MEDR/FORTIS MED/', 'MEDR/MAX HEALTH/', 'MEDR/MANIPAL HSP/'],
    'Pharmacy': ['MEDR/APOLLO PHR/', 'MEDR/MEDPLUS/', 'MEDR/NETMEDS/', 'MEDR/1MG PHARM/'],
    'Movie': ['MEDR/PVR CINEMA/', 'MEDR/INOX/', 'MEDR/CINEPOLIS/', 'MEDR/BOOKMYSHOW/'],
    'Travel': ['MEDR/IRCTC/', 'MEDR/MAKEMYTRIP/', 'MEDR/GOIBIBO/', 'MEDR/YATRA TRV/'],
    'Metro': ['MEDR/METRO CARD/', 'MEDR/DMRC/', 'MEDR/BMRC METRO/', 'MEDR/METRO RCH/'],
    'Cab': ['MEDR/OLA CABS/', 'MEDR/UBER/', 'MEDR/RAPIDO/', 'MEDR/MERU CABS/'],
    'School Fees': ['MEDR/SCHOOL FEE/', 'MEDR/TUITION/', 'MEDR/EDUCATION/', 'MEDR/SCH ADMIS/'],
    'Insurance': ['MEDR/LIC PREM/', 'MEDR/HDFC LIFE/', 'MEDR/ICICI PRU/', 'MEDR/HEALTH INS/'],
    'Rent': ['NEFT-HOUSE RENT', 'NEFT-FLAT RENT', 'NEFT-RENT PAYMENT', 'NEFT-MONTHLY RENT']
}

ATM_IDS = ['CSO9013', 'ID046101', 'CS046112', 'MSO9047', 'TPCN1257', 'NKOL6146', 'DWCW278', 'CPCN0170']

def generate_customer_details():
    """Generate unique BOI customer details"""
    # Ensure unique name combination
    max_attempts = 100
    for _ in range(max_attempts):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        full_name = f"{first.upper()} {last.upper()}"
        
        if full_name not in USED_NAMES:
            USED_NAMES.add(full_name)
            break
    else:
        # If all combinations exhausted, create unique name with number
        full_name = f"{random.choice(FIRST_NAMES).upper()} {random.choice(LAST_NAMES).upper()} {len(USED_NAMES)}"
        USED_NAMES.add(full_name)
    
    city = random.choice(CITIES)
    locality = random.choice(LOCALITIES)
    first_name_part = full_name.split()[0]
    
    return {
        'branch': random.choice(BOI_BRANCHES),
        'name': full_name,
        'address1': f"{random.randint(1, 999)}, {first_name_part}YO {locality}, {first_name_part}WAS",
        'address2': f"DIST {city.upper()}",
        'address3': f"{random.choice(['MAIN ROAD', 'STATION AREA', 'CIVIL LINES', 'MARKET AREA'])} (DIST {city.upper()})",
        'account_no': f"{random.randint(100000000000, 999999999999)}",
        'customer_id': f"{random.randint(100000000, 999999999)}",
        'ifsc': f"BKID000{random.randint(1000, 9999)}",
        'micr': f"{random.randint(400000000, 700999999)}",
    }

def generate_boi_transactions(start_date, end_date, opening_balance, num_transactions=300):
    """Generate BOI-style transactions with expense categories - ensures positive balance"""
    transactions = []
    current_date = start_date
    balance = opening_balance
    day_counter = 0
    salary_day = random.randint(1, 5)
    
    sl_no = 1
    
    # Ensure opening balance is sufficient
    if balance < 20000:
        balance = round(random.uniform(50000, 150000), 2)
    
    # Flatten expense categories for rotation
    all_expenses = []
    for category, merchants in EXPENSE_CATEGORIES.items():
        all_expenses.extend([(category, m) for m in merchants])
    random.shuffle(all_expenses)
    expense_index = 0
    
    while len(transactions) < num_transactions:
        day_counter += 1
        
        # Monthly salary
        if current_date.day == salary_day and random.random() > 0.2:
            salary = round(random.uniform(35000, 55000), 2)
            balance += salary
            transactions.append({
                'sl_no': sl_no,
                'date': current_date.strftime('%d-%m-%Y'),
                'description': random.choice(['salary', 'SALARY CREDIT', 'SAL CREDIT']),
                'cheque_no': '',
                'withdrawal': '',
                'deposit': f"{salary:,.2f}",
                'balance': f"{balance:,.2f}"
            })
            sl_no += 1
            
            # Loan recovery after salary
            if random.random() > 0.4 and len(transactions) < num_transactions:
                loan_amt = round(random.uniform(8000, 15000), 2)
                balance -= loan_amt
                transactions.append({
                    'sl_no': sl_no,
                    'date': current_date.strftime('%d-%m-%Y'),
                    'description': random.choice(['LOAN RECOVERY', 'Loan amt debit', 'loan rec']),
                    'cheque_no': '',
                    'withdrawal': f"{loan_amt:,.2f}",
                    'deposit': '',
                    'balance': f"{balance:,.2f}"
                })
                sl_no += 1
        
        # Quarterly interest
        if current_date.day == 10 and current_date.month in [1, 4, 7, 10] and random.random() > 0.5:
            interest = round(random.uniform(50, 200), 2)
            prev_start = (current_date - timedelta(days=90)).strftime('%d-%m-%Y')
            prev_end = (current_date - timedelta(days=1)).strftime('%d-%m-%Y')
            balance += interest
            transactions.append({
                'sl_no': sl_no,
                'date': current_date.strftime('%d-%m-%Y'),
                'description': f"Int:{prev_start}/{prev_end}",
                'cheque_no': '',
                'withdrawal': '',
                'deposit': f"{interest:,.2f}",
                'balance': f"{balance:,.2f}"
            })
            sl_no += 1
        
        # Daily transactions
        num_daily = random.randint(1, 4)
        
        for _ in range(num_daily):
            if len(transactions) >= num_transactions:
                break
            
            trans_type = random.choices(['expense', 'atm', 'upi', 'neft', 'nach', 'charges'], 
                                       weights=[0.35, 0.25, 0.2, 0.08, 0.05, 0.07])[0]
            
            if trans_type == 'expense':
                # Skip if balance too low
                if balance < 5000:
                    continue
                    
                # Category-based expenses
                category, merchant = all_expenses[expense_index % len(all_expenses)]
                expense_index += 1
                
                # Different amount ranges per category
                if category in ['Rent', 'School Fees', 'Insurance']:
                    amount = round(random.uniform(5000, min(20000, balance * 0.15)), 2)
                elif category in ['Grocery', 'Fuel', 'Medical']:
                    amount = round(random.uniform(500, min(3000, balance * 0.1)), 2)
                elif category in ['Restaurant', 'Swiggy', 'Zomato', 'Movie']:
                    amount = round(random.uniform(200, min(1500, balance * 0.05)), 2)
                else:
                    amount = round(random.uniform(100, min(2000, balance * 0.08)), 2)
                
                # Ensure balance stays positive
                if amount >= balance:
                    amount = round(balance * 0.1, 2)
                    if amount < 10:
                        continue
                
                ref = random.randint(100000, 999999)
                description = f"{merchant}{ref}/"
                balance -= amount
                
                transactions.append({
                    'sl_no': sl_no,
                    'date': current_date.strftime('%d-%m-%Y'),
                    'description': description,
                    'cheque_no': '',
                    'withdrawal': f"{amount:,.2f}",
                    'deposit': '',
                    'balance': f"{balance:,.2f}"
                })
                sl_no += 1
            
            elif trans_type == 'atm':
                # Skip if balance too low
                if balance < 2000:
                    continue
                    
                # ATM withdrawal
                amount = round(random.uniform(500, min(7500, balance * 0.2)), 2)
                
                # Ensure balance stays positive
                if amount >= balance:
                    amount = round(balance * 0.15, 2)
                    if amount < 100:
                        continue
                atm_id = random.choice(ATM_IDS)
                ref = random.randint(100000, 999999)
                description = f"CWDR//{ref}/{atm_id}"
                balance -= amount
                
                transactions.append({
                    'sl_no': sl_no,
                    'date': current_date.strftime('%d-%m-%Y'),
                    'description': description,
                    'cheque_no': '',
                    'withdrawal': f"{amount:,.2f}",
                    'deposit': '',
                    'balance': f"{balance:,.2f}"
                })
                sl_no += 1
                
                # Occasional reversal
                if random.random() > 0.96 and len(transactions) < num_transactions:
                    balance += amount
                    transactions.append({
                        'sl_no': sl_no,
                        'date': current_date.strftime('%d-%m-%Y'),
                        'description': f"CWRR//{ref}/{atm_id}",
                        'cheque_no': '',
                        'withdrawal': '',
                        'deposit': f"{amount:,.2f}",
                        'balance': f"{balance:,.2f}"
                    })
                    sl_no += 1
            
            elif trans_type == 'upi':
                # Skip if balance too low
                if balance < 1000:
                    continue
                    
                # UPI transaction
                amount = round(random.uniform(50, min(2500, balance * 0.1)), 2)
                
                # Ensure balance stays positive
                if amount >= balance:
                    amount = round(balance * 0.08, 2)
                    if amount < 50:
                        continue
                ref = random.randint(700000000000, 799999999999)
                hour = random.randint(0, 23)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                timestamp = f"{hour:02d}:{minute:02d}:{second:02d}"
                date_str = current_date.strftime('%d-%m-%Y')
                
                description = f"BUPI/{ref}/{date_str}\n{timestamp}/UPI"
                balance -= amount
                
                transactions.append({
                    'sl_no': sl_no,
                    'date': current_date.strftime('%d-%m-%Y'),
                    'description': description,
                    'cheque_no': '',
                    'withdrawal': f"{amount:,.2f}",
                    'deposit': '',
                    'balance': f"{balance:,.2f}"
                })
                sl_no += 1
            
            elif trans_type == 'neft':
                # NEFT credit
                amount = round(random.uniform(500, 5000), 2)
                sender = random.choice(['REFUND', 'TRANSFER', 'PAYMENT', 'REIMBURSEMENT'])
                description = f"NEFT-{sender}"
                balance += amount
                
                transactions.append({
                    'sl_no': sl_no,
                    'date': current_date.strftime('%d-%m-%Y'),
                    'description': description,
                    'cheque_no': '',
                    'withdrawal': '',
                    'deposit': f"{amount:,.2f}",
                    'balance': f"{balance:,.2f}"
                })
                sl_no += 1
            
            elif trans_type == 'nach':
                # Skip if balance too low
                if balance < 8000:
                    continue
                    
                # NACH debit
                amount = round(random.uniform(5000, min(12000, balance * 0.2)), 2)
                
                # Ensure balance stays positive
                if amount >= balance:
                    continue
                bank = random.choice(['HDFC BANK LIMITED', 'ICICI BANK', 'SBI', 'AXIS BANK'])
                ref = random.randint(1000000000, 9999999999)
                description = f"NACH DR INW - {bank}\n/ {ref} / AGL"
                balance -= amount
                
                transactions.append({
                    'sl_no': sl_no,
                    'date': current_date.strftime('%d-%m-%Y'),
                    'description': description,
                    'cheque_no': '',
                    'withdrawal': f"{amount:,.2f}",
                    'deposit': '',
                    'balance': f"{balance:,.2f}"
                })
                sl_no += 1
            
            elif trans_type == 'charges':
                # Skip if balance too low
                if balance < 500:
                    continue
                    
                # Bank charges
                amount = round(random.uniform(10, min(100, balance * 0.01)), 2)
                charges = random.choice([
                    'SMSChargesQtrAPR24-JUN24+GST@18',
                    'Annual Maintenance Charges',
                    'Debit Card Annual Charges',
                    'Service Charges'
                ])
                balance -= amount
                
                transactions.append({
                    'sl_no': sl_no,
                    'date': current_date.strftime('%d-%m-%Y'),
                    'description': charges,
                    'cheque_no': '',
                    'withdrawal': f"{amount:,.2f}",
                    'deposit': '',
                    'balance': f"{balance:,.2f}"
                })
                sl_no += 1
        
        # Move to next day
        current_date += timedelta(days=1)
        if current_date > end_date:
            current_date = start_date + timedelta(days=day_counter % 365)
    
    return transactions[:num_transactions], balance

def create_boi_statement_pdf(customer, transactions, opening_balance, closing_balance, start_date, end_date, filename):
    """Create Bank of India statement PDF matching exact format"""
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    styles = getSampleStyleSheet()
    
    # Plain text styles (NO HTML tags)
    plain_style = ParagraphStyle(
        'Plain',
        parent=styles['Normal'],
        fontSize=8,
        fontName='Helvetica',
        alignment=TA_LEFT,
        leading=10
    )
    
    bold_style = ParagraphStyle(
        'Bold',
        parent=styles['Normal'],
        fontSize=8,
        fontName='Helvetica-Bold',
        alignment=TA_LEFT,
        leading=10
    )
    
    small_style = ParagraphStyle(
        'Small',
        parent=styles['Normal'],
        fontSize=6,
        fontName='Helvetica',
        alignment=TA_LEFT,
        leading=8
    )
    
    # BANK NAME - exactly as required
    bank_name_style = ParagraphStyle(
        'BankName',
        parent=styles['Normal'],
        fontSize=12,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
        spaceAfter=10
    )
    elements.append(Paragraph("BANK OF INDIA", bank_name_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Branch and date
    elements.append(Paragraph(customer['branch'], bold_style))
    elements.append(Paragraph(f"Date: {datetime.now().strftime('%d/%m/%Y')}", plain_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Customer details
    elements.append(Paragraph(f"Name : {customer['name']}", bold_style))
    elements.append(Paragraph(f"Address : {customer['address1']}", plain_style))
    elements.append(Paragraph(customer['address2'], plain_style))
    elements.append(Paragraph(customer['address3'], plain_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Account details - EXACT format
    elements.append(Paragraph(f"Account No        : {customer['account_no']}", plain_style))
    elements.append(Paragraph(f"Customer ID       : {customer['customer_id']}", plain_style))
    elements.append(Paragraph(f"Account Type      : Savings Account", plain_style))
    elements.append(Paragraph(f"IFSC Code         : {customer['ifsc']}", plain_style))
    elements.append(Paragraph(f"MICR Code         : {customer['micr']}", plain_style))
    
    # Statement header - moved BELOW MICR Code
    elements.append(Paragraph(
        f"Account Statement: For the period {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}",
        bold_style
    ))
    elements.append(Spacer(1, 0.1*inch))
    
    # Statement generation info
    gen_time = datetime.now().strftime('%d/%m/%Y %I:%M:%S %p')
    elements.append(Paragraph(f"Statement Generated on : {gen_time}.", plain_style))
    elements.append(Paragraph("This is a computer generated statement and hence no signature required", small_style))
    
    # Disclaimers
    elements.append(Paragraph("Please provide your contact details, Mobile number, PAN Card, Aadhar Card, Date of Birth to help you serve better.", small_style))
    elements.append(Paragraph("Any discrepancy in this document of accounts should be notified to the bank within a period of 30 days of receipt of this statement.", small_style))
    elements.append(Paragraph("It will be treated that the entries/contents of this statement are checked and found correct by you, if no such complaint is madewithin the period stated above.", small_style))
    elements.append(Paragraph("Beware of fictitious offers, messages/SMS about lottery winnings, cheap fund offers, employment offers, scholarship offers, offer of immigration visas, offer of admission to reputed universities abroad and similar such offers from fraudsters either within the country or from abroad.", small_style))
    elements.append(Paragraph("For any support or clarification please contact Call Centre No.1800 220 229, 1800 103 1906, 022 40919191.", small_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Transaction table
    trans_data = [['Sl No', 'Txn Date', 'Description', 'Cheque No', 'Withdrawal\n(in Rs.)', 'Deposits\n(in Rs.)', 'Balance\n(in Rs.)']]
    
    for trans in transactions:
        trans_data.append([
            str(trans['sl_no']),
            trans['date'],
            trans['description'],
            trans['cheque_no'],
            trans['withdrawal'],
            trans['deposit'],
            trans['balance']
        ])
    
    # Create table
    trans_table = Table(trans_data, colWidths=[0.4*inch, 0.7*inch, 2.2*inch, 0.6*inch, 0.8*inch, 0.8*inch, 0.9*inch])
    trans_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 6),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (2, -1), 'LEFT'),
        ('ALIGN', (3, 0), (3, -1), 'CENTER'),
        ('ALIGN', (4, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9)),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
    ]))
    
    elements.append(trans_table)
    elements.append(Spacer(1, 0.1*inch))
    
    # Footer disclaimers (repeated)
    elements.append(Paragraph(f"Statement Generated on : {gen_time}.", plain_style))
    elements.append(Paragraph("This is a computer generated statement and hence no signature required.", small_style))
    elements.append(Paragraph("Please provide your contact details, Mobile number, PAN Card, Aadhar Card, Date of Birth to help you serve better.", small_style))
    elements.append(Paragraph("Any discrepancy in this document of accounts should be notified to the bank within a period of 30 days of receipt of this statement.", small_style))
    elements.append(Paragraph("It will be treated that the entries/contents of this statement are checked and found correct by you, if no such complaint is madewithin the period stated above.", small_style))
    elements.append(Paragraph("Beware of fictitious offers, messages/SMS about lottery winnings, cheap fund offers, employment offers, scholarship offers, offer of immigration visas, offer of admission to reputed universities abroad and similar such offers from fraudsters either within the country or from abroad.", small_style))
    elements.append(Paragraph("For any support or clarification please contact Call Centre No.1800 220 229, 1800 103 1906, 022 40919191.", small_style))
    
    doc.build(elements)

def generate_statements_batch(num_statements, num_transactions, output_dir, start_date, end_date):
    """Generate a batch of BOI statements with specified number of transactions"""
    print(f"\n{'='*70}")
    print(f"  Generating {num_statements} statements with {num_transactions} entries each")
    print(f"{'='*70}")
    
    for i in range(1, num_statements + 1):
        print(f"[{i}/{num_statements}] Generating {num_transactions}-entry statement...")
        
        # Generate unique customer
        customer = generate_customer_details()
        
        # Higher opening balance to ensure positive balance throughout
        opening_balance = round(random.uniform(150000, 300000), 2)
        
        # Generate transactions
        transactions, closing_balance = generate_boi_transactions(
            start_date, end_date, opening_balance, num_transactions=num_transactions
        )
        
        # Create filename
        filename = os.path.join(
            output_dir, 
            f"BOI_Statement_{customer['name'].replace(' ', '_')}_{num_transactions}_Entries.pdf"
        )
        
        # Generate PDF
        create_boi_statement_pdf(customer, transactions, opening_balance, closing_balance, start_date, end_date, filename)
        print(f"    ✅ Generated: {os.path.basename(filename)}")

def main():
    """Main function to generate BOI statements with both 150 and 300 entries"""
    print("\n" + "="*70)
    print("        BANK OF INDIA - COMBINED STATEMENT GENERATOR")
    print("="*70)
    print("\n🔄 Generating 10 PDFs with 300 entries + 10 PDFs with 150 entries\n")
    print("✨ All 20 PDFs will have unique customer names\n")
    
    # Clear used names set to start fresh
    USED_NAMES.clear()
    
    # Updated paths to match BANKFUSION directory structure
    # Script is in: data/synthetic_templates/Bank/bank_of_india_generator.py
    # PDFs go to: data/raw_pdfs/bank_of_india/
    output_dir = "../../../data/raw_pdfs/bank_of_india"
    # output_dir_150 = os.path.join(base_output_dir, "150_entries")
    # output_dir_300 = os.path.join(base_output_dir, "300_entries")
    
    # Create directories if they don't exist
    os.makedirs(output_dir, exist_ok=True)
    # os.makedirs(output_dir, exist_ok=True)
    
    start_date = datetime(2024, 4, 1)
    end_date = datetime(2025, 3, 31)
    
    # Generate 10 statements with 300 entries
    generate_statements_batch(10, 300, output_dir, start_date, end_date)
    
    # Generate 10 statements with 150 entries
    generate_statements_batch(10, 150, output_dir, start_date, end_date)
    
    print("\n" + "="*70)
    print("✅ SUCCESS! Generated all Bank of India statements")
    print("="*70)
    print(f"\n📁 300-Entry Statements: {os.path.abspath(output_dir)}/")
    print(f"   • 10 PDFs with 300 transactions each")
    print(f"\n📁 150-Entry Statements: {os.path.abspath(output_dir)}/")
    print(f"   • 10 PDFs with 150 transactions each")
    print(f"\n💰 All balances remain positive throughout")
    print(f"🏦 BOI format with BANK OF INDIA header")
    print(f"💵 Realistic expense categories in descriptions")
    print(f"📊 Total PDFs generated: 20 (all with unique names)")
    print(f"👥 Unique customers: {len(USED_NAMES)}")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()