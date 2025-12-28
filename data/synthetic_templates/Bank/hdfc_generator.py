"""
HDFC Bank Statement PDF Generator - Multi-Bank Statement Normalization Engine
Generates 20 realistic synthetic bank statements (10 with 300 txns, 10 with 150 txns)
WARNING: For testing/training purposes ONLY. Misuse is illegal.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from datetime import datetime, timedelta
import random
import os

# ==================== DATA TEMPLATES ====================

INDIAN_FIRST_NAMES = [
    'RAJESH', 'PRIYA', 'AMIT', 'SNEHA', 'VIKAS', 'ANJALI', 'RAHUL', 'KAVITA',
    'MANOJ', 'DEEPA', 'SURESH', 'POOJA', 'ARUN', 'MEERA', 'SANDEEP', 'RITU',
    'VIJAY', 'NEHA', 'ASHOK', 'SUNITA', 'KIRAN', 'ANITA', 'RAMESH', 'SEEMA'
]

INDIAN_LAST_NAMES = [
    'KUMAR', 'SHARMA', 'PATEL', 'VERMA', 'SINGH', 'GUPTA', 'MEHTA', 'SHAH',
    'REDDY', 'IYER', 'NAIR', 'JOSHI', 'AGARWAL', 'PILLAI', 'MISHRA', 'DUBEY'
]

TRANSACTION_PATTERNS = {
    'food_dining': [
        ('UPI-{ref}-SWIGGY-UPI-{upi}-OK', 150, 800, 'high'),
        ('UPI-{ref}-ZOMATO-UPI-{upi}-OK', 200, 900, 'high'),
        ('POS {card} MCDONALD S POS DEBIT', 150, 500, 'medium'),
        ('POS {card} DOMINOS PIZZA POS DEBIT', 300, 800, 'medium'),
        ('POS {card} KFC RESTAURANT POS DEBIT', 250, 600, 'medium'),
        ('POS {card} CAFE COFFEE DAY POS DEBIT', 100, 350, 'medium'),
        ('POS {card} STARBUCKS COFFEE POS DEBIT', 200, 450, 'medium'),
        ('POS {card} HALDIRAM S POS DEBIT', 150, 400, 'low'),
        ('POS {card} BARBEQUE NATION POS DEBIT', 800, 1800, 'low'),
        ('POS {card} PUNJABI DHABA POS DEBIT', 200, 600, 'medium'),
    ],
    'groceries': [
        ('POS {card} DMART POS DEBIT', 800, 2500, 'high'),
        ('POS {card} RELIANCE FRESH POS DEBIT', 600, 1800, 'high'),
        ('POS {card} BIG BAZAAR POS DEBIT', 1000, 3000, 'medium'),
        ('POS {card} MORE SUPERMARKET POS DEBIT', 500, 1500, 'medium'),
        ('POS {card} SPENCERS RETAIL POS DEBIT', 700, 2000, 'low'),
        ('POS {card} NATURE S BASKET POS DEBIT', 800, 2200, 'low'),
        ('POS {card} LOCAL KIRANA POS DEBIT', 300, 800, 'medium'),
    ],
    'travel': [
        ('UPI-{ref}-UBER INDIA-UPI-{upi}-OK', 80, 600, 'high'),
        ('UPI-{ref}-OLA CABS-UPI-{upi}-OK', 70, 500, 'high'),
        ('POS {card} INDIAN OIL PETROL POS DEBIT', 1000, 3000, 'medium'),
        ('POS {card} BHARAT PETROLEUM POS DEBIT', 1000, 2800, 'medium'),
        ('POS {card} HP PETROL PUMP POS DEBIT', 1200, 2900, 'medium'),
        ('ATW-{card}-{code}-MUMBAI', 200, 500, 'low'),
        ('POS {card} MAKEMYTRIP POS DEBIT', 2000, 15000, 'low'),
        ('POS {card} IRCTC RAIL TICKET POS DEBIT', 500, 3000, 'medium'),
    ],
    'shopping': [
        ('UPI-{ref}-AMAZON PAY-UPI-{upi}-OK', 500, 5000, 'high'),
        ('POS {card} AMAZON PAY POS DEBIT', 600, 4000, 'high'),
        ('POS {card} FLIPKART POS DEBIT', 800, 5000, 'medium'),
        ('POS {card} MYNTRA POS DEBIT', 1000, 3500, 'medium'),
        ('POS {card} LIFESTYLE POS DEBIT', 1200, 4000, 'low'),
        ('POS {card} WESTSIDE POS DEBIT', 900, 2800, 'low'),
        ('POS {card} PANTALOONS POS DEBIT', 1100, 3200, 'low'),
        ('POS {card} SHOPPER S STOP POS DEBIT', 1500, 4500, 'low'),
    ],
    'entertainment': [
        ('POS {card} INOX CINEMAS POS DEBIT', 400, 1200, 'medium'),
        ('POS {card} PVR CINEMAS POS DEBIT', 450, 1300, 'medium'),
        ('UPI-{ref}-BOOKMYSHOW-UPI-{upi}-OK', 300, 1000, 'medium'),
        ('NHDF{ref_num}/BILLDKNETFLIX', 500, 800, 'low'),
        ('NHDF{ref_num}/BILLDKAMAZONPRIME', 999, 1499, 'low'),
        ('NHDF{ref_num}/BILLDKSPOTIFY', 119, 119, 'low'),
        ('NHDF{ref_num}/BILLDKHOTSTAR', 299, 1499, 'low'),
    ],
    'utilities': [
        ('IB BILLPAY DR-HDFCPE-545964XXXXXX3563', 1000, 5000, 'medium'),
        ('NHDF{ref_num}/BILLDKVODAFONEINDIAL', 200, 800, 'high'),
        ('NHDF{ref_num}/BILLDKRELIANCEJIOINF', 300, 700, 'high'),
        ('NHDF{ref_num}/BILLDKAIRTELINDIA', 250, 900, 'high'),
        ('ACH D- TP ACH HOME-{ref_num}', 2000, 3500, 'medium'),
        ('ACH D- HOMECRINDFINPVTLTD-{ref_num}', 1000, 2500, 'low'),
        ('NHDF{ref_num}/BILLDKBESCOM', 800, 3000, 'medium'),
    ],
    'health_fitness': [
        ('POS {card} APOLLO PHARMACY POS DEBIT', 200, 1500, 'medium'),
        ('POS {card} MEDPLUS POS DEBIT', 150, 1200, 'medium'),
        ('UPI-{ref}-PRACTO-UPI-{upi}-OK', 300, 1000, 'low'),
        ('POS {card} GOLD S GYM POS DEBIT', 2000, 5000, 'low'),
        ('POS {card} CULT FIT POS DEBIT', 1000, 3000, 'low'),
    ],
    'transfers_out': [
        ('NEFT DR-{ifsc}-{name}-NETBANK, MUM-{neft_ref}-PERSONAL', 1000, 15000, 'medium'),
        ('IMPS-{imps_ref}-{name}-HDFC-XXXXXXXX{acc}-PERSONAL', 500, 10000, 'medium'),
        ('UPI-{ref}-{name}@UPI-{upi}-OK', 500, 5000, 'high'),
    ],
    'salary_credit': [
        ('NEFT CR-SBIN0001234-{company}-SALARY FOR {month}', 35000, 90000, 'salary'),
        ('IMPS-{imps_ref}-{company}-CORP-SALARY CREDIT', 40000, 95000, 'salary'),
    ],
    'emi': [
        ('EMI {emi_num} CHQ S{chq_num} {date_code}{emi_num}', 2000, 8000, 'medium'),
    ],
    'cash': [
        ('CASH DEP MIRA ROAD -', 5000, 25000, 'low'),
        ('MICRO ATM CASH DEP - HDFC THANE MH IN - BNAKMU02', 3000, 20000, 'low'),
        ('MICRO ATM CASH DEP - HDFC MUMBAI MH IN - BNAKMU29', 2000, 15000, 'low'),
    ],
    'card_bills': [
        ('NHDF{ref_num}/SBI CARDS', 2000, 20000, 'low'),
        ('NHDF{ref_num}/BILLDKKOTAKCARDS', 3000, 15000, 'low'),
        ('NHDF{ref_num}/BILLDKHDFCCARDS', 2500, 12000, 'low'),
    ],
    'interest': [
        ('CREDIT INTEREST CAPITALISED', 50, 300, 'low'),
    ]
}

COMPANIES = [
    'INFOSYS LIMITED', 'TCS LIMITED', 'WIPRO LIMITED', 'ACCENTURE INDIA PVT LTD',
    'HCL TECHNOLOGIES LTD', 'COGNIZANT TECH SOLUTIONS', 'TECH MAHINDRA LTD',
    'CAPGEMINI INDIA PVT LTD', 'L AND T INFOTECH LTD', 'MINDTREE LIMITED'
]

MONTHS_FULL = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 
               'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']

# ==================== TRANSACTION GENERATOR ====================

class TransactionGenerator:
    def __init__(self):
        self.transactions = []
        
    def generate_format_vars(self, txn_date=''):
        """Generate all placeholder variables"""
        return {
            'card': f"416021XXXXXX{random.randint(1000, 9999)}",
            'ref': str(random.randint(100000000000, 999999999999)),
            'upi': str(random.randint(810000000000, 899999999999)),
            'name': f"{random.choice(INDIAN_FIRST_NAMES)} {random.choice(INDIAN_LAST_NAMES)}",
            'ifsc': f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))}{random.randint(100000, 999999)}",
            'neft_ref': f"N{random.randint(100000000000, 999999999999)}",
            'imps_ref': str(random.randint(800000000000, 899999999999)),
            'ref_num': str(random.randint(6000000000, 6999999999)),
            'emi_num': str(random.randint(4900000, 5100000)),
            'chq_num': str(random.randint(490000000, 510000000)),
            'date_code': txn_date.replace('/', ''),
            'acc': str(random.randint(1000, 9999)),
            'code': ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8)),
            'company': random.choice(COMPANIES),
            'month': random.choice(MONTHS_FULL)
        }
    
    def generate_transactions(self, start_date, end_date, num_transactions):
        """Generate realistic human-like transactions"""
        transactions = []
        
        # Parse dates
        start = datetime.strptime(start_date, '%d/%m/%Y')
        end = datetime.strptime(end_date, '%d/%m/%Y')
        
        # Generate all dates in range
        all_dates = []
        current = start
        while current <= end:
            all_dates.append(current.strftime('%d/%m/%y'))
            current += timedelta(days=1)
        
        # Add 2-3 salary credits
        num_salaries = min(2, len(all_dates) // 30 + 1)
        salary_dates = random.sample(all_dates[::28] if len(all_dates) > 28 else all_dates[:1], num_salaries)
        
        for sal_date in salary_dates:
            template = random.choice(TRANSACTION_PATTERNS['salary_credit'])
            amount = random.uniform(template[1], template[2])
            format_vars = self.generate_format_vars(sal_date)
            
            narration = template[0]
            for key, value in format_vars.items():
                narration = narration.replace('{' + key + '}', str(value))
            
            transactions.append({
                'date': sal_date,
                'narration': narration[:65],
                'ref_no': f"{random.randint(10**15, 10**16-1):016d}",
                'value_date': sal_date,
                'withdrawal': '',
                'deposit': f"{amount:.2f}"
            })
        
        # Calculate weights for realistic spending patterns
        category_weights = {
            'food_dining': 25,
            'groceries': 15,
            'travel': 20,
            'shopping': 12,
            'entertainment': 8,
            'utilities': 10,
            'health_fitness': 5,
            'transfers_out': 8,
            'emi': 3,
            'cash': 3,
            'card_bills': 2,
            'interest': 1
        }
        
        # Generate remaining transactions
        remaining = num_transactions - len(transactions)
        
        for _ in range(remaining):
            # Choose category based on weights
            category = random.choices(
                list(category_weights.keys()),
                weights=list(category_weights.values()),
                k=1
            )[0]
            
            templates = TRANSACTION_PATTERNS[category]
            template = random.choice(templates)
            
            # Choose date based on transaction frequency
            if template[3] == 'high':  # Frequent transactions
                txn_date = random.choice(all_dates)
            elif template[3] == 'medium':
                txn_date = random.choice(all_dates[::2] if len(all_dates) > 2 else all_dates)
            else:  # Low frequency
                txn_date = random.choice(all_dates[::5] if len(all_dates) > 5 else all_dates)
            
            # Generate amount with some variance
            base_amount = random.uniform(template[1], template[2])
            # Add 10% variance for realism
            amount = base_amount * random.uniform(0.90, 1.10)
            
            format_vars = self.generate_format_vars(txn_date)
            
            narration = template[0]
            for key, value in format_vars.items():
                narration = narration.replace('{' + key + '}', str(value))
            
            # Determine if withdrawal or deposit
            is_deposit = category in ['salary_credit', 'cash', 'interest']
            if category == 'transfers_out' and random.random() < 0.15:  # 15% chance of receiving money
                is_deposit = True
            
            transactions.append({
                'date': txn_date,
                'narration': narration[:65],
                'ref_no': f"{random.randint(10**15, 10**16-1):016d}",
                'value_date': txn_date,
                'withdrawal': '' if is_deposit else f"{amount:.2f}",
                'deposit': f"{amount:.2f}" if is_deposit else ''
            })
        
        # Sort by date
        transactions.sort(key=lambda x: datetime.strptime(x['date'], '%d/%m/%y'))
        
        return transactions

# ==================== PDF GENERATOR ====================

class HDFCStatementPDF:
    def __init__(self, filename, output_dir=None):
        # FIXED: Use ../../../data/raw_pdfs/HDFC relative to script location
        if output_dir is None:
            # This will point to BANKFUSION/data/raw_pdfs/HDFC
            output_dir = "../../../data/raw_pdfs/HDFC"
        
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.filename = os.path.join(output_dir, filename)
        print(f"📁 Saving to: {os.path.abspath(self.output_dir)}")
        self.pages = []
        
    def add_watermark(self, canvas_obj, doc):
        """Add SAMPLE watermark"""
        canvas_obj.saveState()
        canvas_obj.setFont('Helvetica-Bold', 70)
        canvas_obj.setFillColorRGB(1, 0, 0, alpha=0.06)
        canvas_obj.translate(A4[0]/2, A4[1]/2)
        canvas_obj.rotate(45)
        canvas_obj.drawCentredString(0, 0, "SAMPLE")
        canvas_obj.restoreState()
        
        # Add page number
        page_num = canvas_obj.getPageNumber()
        canvas_obj.setFont('Helvetica', 7)
        canvas_obj.setFillColorRGB(0, 0, 0)
        canvas_obj.drawRightString(A4[0] - 15*mm, A4[1] - 10*mm, f"Page No.: {page_num}")
    
    def create_header(self, account_data, page_num):
        """Create page header"""
        elements = []
        
        # Bank title
        title_style = ParagraphStyle('Title', fontName='Helvetica-Bold', fontSize=14,
                                     textColor=colors.HexColor('#004B87'), leading=16)
        
        title_data = [[
            Paragraph('HDFC BANK LIMITED', title_style),
            Paragraph(f'Generated: {datetime.now().strftime("%d-%b-%Y")}',
                     ParagraphStyle('r', fontName='Helvetica', fontSize=7, alignment=TA_RIGHT))
        ]]
        
        title_table = Table(title_data, colWidths=[470, 70])
        title_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.HexColor('#004B87')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(title_table)
        elements.append(Spacer(1, 2*mm))
        
        # Statement subtitle
        elements.append(Paragraph('<b>Statement of account</b>',
                                 ParagraphStyle('sub', fontName='Helvetica-Bold', fontSize=8)))
        elements.append(Spacer(1, 3*mm))
        
        # Account information
        left_col = f"""<b>MR. {account_data['name']}</b><br/>
{account_data['address1']}<br/>
{account_data['address2']}<br/>
{account_data['address3']}<br/>
{account_data['city']}<br/>
{account_data['state']} INDIA"""
        
        right_col = f"""<b>Account No:</b> {account_data['account_no']}<br/>
<b>Branch:</b> {account_data['branch']}<br/>
<b>IFSC:</b> {account_data['ifsc']}<br/>
<b>Account Type:</b> SAVINGS<br/>
<b>Period:</b> {account_data['from_date']} To {account_data['to_date']}<br/>
<b>Currency:</b> INR<br/>
<b>Nomination:</b> Registered"""
        
        info_style = ParagraphStyle('info', fontName='Helvetica', fontSize=7, leading=9)
        
        info_data = [[Paragraph(left_col, info_style), Paragraph(right_col, info_style)]]
        info_table = Table(info_data, colWidths=[275, 265])
        info_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 4*mm))
        
        return elements
    
    def create_transaction_table(self, transactions):
        """Create transaction table"""
        # Header
        header_style = ParagraphStyle('h', fontName='Helvetica-Bold', fontSize=6.5,
                                     alignment=TA_CENTER, textColor=colors.white, leading=8)
        
        table_data = [[
            Paragraph('<b>Date</b>', header_style),
            Paragraph('<b>Narration</b>', header_style),
            Paragraph('<b>Chq./Ref.No.</b>', header_style),
            Paragraph('<b>Value Dt</b>', header_style),
            Paragraph('<b>Withdrawal Amt.</b>', header_style),
            Paragraph('<b>Deposit Amt.</b>', header_style),
            Paragraph('<b>Closing Balance</b>', header_style),
        ]]
        
        # Data rows
        cell_style = ParagraphStyle('cell', fontName='Helvetica', fontSize=6.5, leading=8)
        right_style = ParagraphStyle('r', fontName='Helvetica', fontSize=6.5,
                                    alignment=TA_RIGHT, leading=8)
        
        for txn in transactions:
            table_data.append([
                Paragraph(txn['date'], cell_style),
                Paragraph(txn['narration'], cell_style),
                Paragraph(txn['ref_no'], cell_style),
                Paragraph(txn['value_date'], cell_style),
                Paragraph(txn.get('withdrawal', ''), right_style),
                Paragraph(txn.get('deposit', ''), right_style),
                Paragraph(txn['balance'], right_style),
            ])
        
        col_widths = [45, 180, 75, 40, 60, 55, 65]
        trans_table = Table(table_data, colWidths=col_widths, repeatRows=1)
        
        trans_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#004B87')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 1), (3, -1), 'LEFT'),
            ('ALIGN', (4, 1), (-1, -1), 'RIGHT'),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#004B87')),
            ('LINEBELOW', (0, 1), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.grey),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        return trans_table
    
    def generate(self, account_data, transactions, opening_balance):
        """Generate complete multi-page PDF"""
        
        # Calculate balances
        balance = float(opening_balance.replace(',', ''))
        for txn in transactions:
            withdrawal = float(txn.get('withdrawal', 0) or 0)
            deposit = float(txn.get('deposit', 0) or 0)
            balance = balance - withdrawal + deposit
            txn['balance'] = f"{balance:,.2f}"
        
        closing_balance = balance
        
        # Split transactions into pages (30 per page for clean layout)
        page_size = 30
        transaction_pages = [transactions[i:i+page_size] for i in range(0, len(transactions), page_size)]
        
        doc = SimpleDocTemplate(
            self.filename,
            pagesize=A4,
            rightMargin=12*mm,
            leftMargin=12*mm,
            topMargin=12*mm,
            bottomMargin=15*mm
        )
        
        story = []
        
        for page_num, page_txns in enumerate(transaction_pages, 1):
            # Add header for each page
            story.extend(self.create_header(account_data, page_num))
            
            # Add transactions
            story.append(self.create_transaction_table(page_txns))
            story.append(Spacer(1, 3*mm))
            
            # Add page break except for last page
            if page_num < len(transaction_pages):
                story.append(PageBreak())
        
        # Add summary on last page
        total_withdrawals = sum(float(t.get('withdrawal', 0) or 0) for t in transactions)
        total_deposits = sum(float(t.get('deposit', 0) or 0) for t in transactions)
        dr_count = sum(1 for t in transactions if float(t.get('withdrawal', 0) or 0) > 0)
        cr_count = sum(1 for t in transactions if float(t.get('deposit', 0) or 0) > 0)
        
        summary_text = f"""<b>STATEMENT SUMMARY:-</b><br/>
Opening Balance: {opening_balance} | Dr Count: {dr_count} | Cr Count: {cr_count} | Debits: {total_withdrawals:,.2f} | Credits: {total_deposits:,.2f} | Closing Balance: {closing_balance:,.2f}"""
        
        story.append(Paragraph(summary_text,
                              ParagraphStyle('sum', fontName='Helvetica', fontSize=7, leading=9)))
        story.append(Spacer(1, 4*mm))
        
        # Footer
        footer_text = """<b>IMPORTANT LEGAL NOTICE:</b> This is a SAMPLE document for testing/training purposes ONLY.
<b>DO NOT USE</b> for official, legal, or financial purposes. Misuse is ILLEGAL.<br/><br/>
*Closing balance includes funds earmarked for hold and uncleared funds.<br/>
Contents of this statement will be considered correct if no error is reported within 30 days.<br/>
This is a computer generated statement and does not require signature.<br/><br/>
HDFC Bank Limited - Registered Office: HDFC Bank House, Senapati Bapat Marg, Lower Parel, Mumbai 400013"""
        
        story.append(Paragraph(footer_text,
                              ParagraphStyle('foot', fontName='Helvetica', fontSize=6, leading=7)))
        
        # Build PDF
        try:
            doc.build(story, onFirstPage=self.add_watermark, onLaterPages=self.add_watermark)
            
            # Verify file was created
            if os.path.exists(self.filename):
                file_size = os.path.getsize(self.filename) / 1024  # Size in KB
                print(f"✓ Created ({file_size:.1f} KB)")
            else:
                print(f"❌ ERROR: File not created!")
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            raise
        
        return closing_balance

# ==================== ACCOUNT GENERATOR ====================

def generate_random_account(statement_num):
    """Generate random account details"""
    societies = ['JUPITER', 'VENUS', 'MARS', 'NEPTUNE', 'MERCURY', 'ORCHID', 'ROSE', 'LOTUS']
    areas = ['MIRA ROAD', 'ANDHERI', 'BORIVALI', 'THANE', 'MULUND', 'KANDIVALI', 'MALAD', 'GOREGAON']
    
    name = f"{random.choice(INDIAN_FIRST_NAMES)} {random.choice(INDIAN_LAST_NAMES)}"
    
    # Generate date range (4 months period)
    start_month = random.randint(1, 8)
    start_date = datetime(2024, start_month, 1)
    end_date = start_date + timedelta(days=120)
    
    return {
        'name': name,
        'address1': f"{random.choice(['A', 'B', 'C'])}/{random.randint(101, 999)} {random.choice(societies)} {random.choice(['A', 'B'])} CHS LTD",
        'address2': f"{random.choice(areas)} {random.choice(['EAST', 'WEST'])}",
        'address3': f"OPP {random.choice(['TANWAR', 'CITY', 'METRO'])} HOSPITAL {random.choice(areas)} EAST",
        'city': f"THANE {random.randint(401101, 401210)}",
        'state': 'MAHARASHTRA',
        'account_no': f"501001{random.randint(10000000, 99999999)}",
        'branch': f"{random.choice(areas)} - KASTURI UDYOG",
        'ifsc': f"HDFC000{random.randint(1000, 9999)}",
        'from_date': start_date.strftime('%d/%m/%Y'),
        'to_date': end_date.strftime('%d/%m/%Y')
    }

# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    print("=" * 80)
    print("HDFC BANK STATEMENT GENERATOR - Multi-Bank Statement Normalization Engine")
    print("=" * 80)
    print("\n⚠️  WARNING: SAMPLE documents for TESTING/TRAINING ONLY")
    print("    Using fake statements for fraud is a SERIOUS CRIME\n")
    print("Generating 20 synthetic bank statements:")
    print("  • 10 statements with 300 transactions each")
    print("  • 10 statements with 150 transactions each")
    print("=" * 80)
    
    generator = TransactionGenerator()
    
    # Configuration
    configs = [(300, 10), (150, 10)]
    
    statement_num = 1
    
    for num_txns, count in configs:
        print(f"\n📊 Generating {count} statements with {num_txns} transactions each...")
        
        for i in range(count):
            print(f"   Statement {statement_num:02d}/20... ", end="", flush=True)
            
            # Generate account data
            account_data = generate_random_account(statement_num)
            
            # Generate transactions
            transactions = generator.generate_transactions(
                account_data['from_date'],
                account_data['to_date'],
                num_txns
            )
            
            # Random opening balance
            opening_balance = f"{random.uniform(8000, 30000):,.2f}"
            
            # Generate PDF
            pdf_name = f"Statement_{statement_num:02d}.pdf"
            pdf = HDFCStatementPDF(pdf_name)
            closing_bal = pdf.generate(account_data, transactions, opening_balance)
            
            statement_num += 1
    
    print("\n" + "=" * 80)
    print("✅ SUCCESS! All 20 statements generated")
    print("=" * 80)