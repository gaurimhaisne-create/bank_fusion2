"""
Union Bank Statement Generator
Generates synthetic bank statements matching the exact structure of Union Bank format
"""

import os
import random
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.pdfgen import canvas

# Indian Names Database
FIRST_NAMES = [
    "ABDUL", "MOHAMMED", "RAHUL", "PRIYA", "AMIT", "SNEHA", "RAJESH", "DEEPAK",
    "ARUN", "VIJAY", "SURESH", "ANITA", "KAVITA", "SANJAY", "RAVI", "POOJA",
    "RAMESH", "KIRAN", "NIKHIL", "SWATI", "MANOJ", "NEHA", "ASHOK", "DIVYA"
]

LAST_NAMES = [
    "KUMAR", "SHARMA", "PATEL", "SINGH", "REDDY", "NAIR", "MENON", "VERMA",
    "GUPTA", "IYER", "RAO", "PILLAI", "KHAN", "DESAI", "JOSHI", "SHAH"
]

CITIES = [
    "KASARAGOD", "KANNUR", "KOZHIKODE", "THRISSUR", "KOCHI", "KOLLAM",
    "THIRUVANANTHAPURAM", "MALAPPURAM", "PALAKKAD", "ALAPPUZHA"
]

# Transaction Templates
UPI_MERCHANTS = [
    ("Swiggy", "SWIGGY/SBIN/swiggy@sbi", 150, 800),
    ("Zomato", "ZOMATO/HDFC/zomato@hdfcbank", 200, 900),
    ("Amazon", "AMAZON/ICICI/amazon@icici", 300, 5000),
    ("Flipkart", "FLIPKART/AXIS/flipkart@axisbank", 400, 6000),
    ("DMart", "DMART/HDFC/dmart@hdfcbank", 500, 3000),
    ("Reliance", "RELIANCE/SBIN/reliance@sbi", 400, 4000),
    ("BPCL Fuel", "BPCL/CNRB/bpcl@canara", 800, 2500),
    ("Indian Oil", "INDIANOIL/YESB/indianoil@ybl", 700, 2200),
    ("Uber", "UBER/UTIB/uber@axisbank", 50, 500),
    ("Ola", "OLA/ICICI/ola@icici", 60, 450),
    ("PhonePe", "PHONEPE/YESB/phonepe@ybl", 10, 2000),
    ("Paytm", "PAYTM/PYTM/paytm@paytm", 20, 1500),
    ("Google Play", "GOOGLEPLAY/UTIB/goog-payment@okaxis", 50, 999),
    ("Netflix", "NETFLIX/HDFC/netflix@hdfcbank", 199, 799),
    ("BookMyShow", "BOOKMYSHOW/ICICI/bookmyshow@icici", 150, 800),
]

PERSON_NAMES = [
    ("RAHUL SHARMA", "RAHUL/SBIN/rahul123@oksbi"),
    ("PRIYA KUMAR", "PRIYA/HDFC/priyak456@okhdfcbank"),
    ("AMIT PATEL", "AMIT/ICICI/amitp789@okicici"),
    ("SNEHA REDDY", "SNEHA/AXIS/snehar@okaxis"),
    ("RAJESH NAIR", "RAJESH/CNRB/rajeshn@okcanara"),
    ("DEEPA MENON", "DEEPA/BARB/deepam@okbob"),
    ("VIJAY SINGH", "VIJAY/FDRL/vijays@okfederal"),
    ("KAVITA VERMA", "KAVITA/KLGB/kavitav@okklgb"),
]

def generate_customer_details():
    """Generate random customer details"""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    middle_initial = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
    city = random.choice(CITIES)
    account_num = f"6722020{random.randint(10000000, 99999999)}"
    mobile = f"91{random.randint(7000000000, 9999999999)}"
    cif_id = random.randint(200000000, 299999999)
    
    return {
        "name": f"{first_name} {middle_initial} {last_name}",
        "address_line1": f"{random.choice(['HOUSE', 'VILLA', 'FLAT'])} NO {random.randint(1, 999)}",
        "address_line2": f"{random.choice(['MAIN ROAD', 'STREET', 'AVENUE'])}",
        "address_line3": city,
        "city": city,
        "state": "KERALA",
        "pincode": random.randint(670000, 695999),
        "mobile": mobile,
        "email": f"{first_name.lower()}{random.randint(100, 999)}@gmail.com",
        "account_number": account_num,
        "cif_id": cif_id,
        "ifsc": "UBIN0567221",
    }

def generate_transaction_id():
    """Generate realistic transaction ID"""
    prefix = random.choice(['S', 'C'])
    return f"{prefix}{random.randint(10000000, 99999999)}"

def generate_transactions(num_transactions, start_date, end_date, opening_balance):
    """Generate realistic transactions with proper financial logic"""
    transactions = []
    current_balance = opening_balance
    
    # Calculate date range
    delta = end_date - start_date
    
    # Generate salary credit (1-2 per period)
    salary_dates = sorted([start_date + timedelta(days=random.randint(0, delta.days)) 
                          for _ in range(random.randint(1, 2))])
    
    for sal_date in salary_dates:
        tran_id = generate_transaction_id()
        salary_amt = random.randint(35000, 85000)
        current_balance += salary_amt
        transactions.append({
            "tran_id": tran_id,
            "date": sal_date,
            "description": f"NEFT:SALARY CREDIT\nFDRLM{random.randint(8000000000, 8999999999)}",
            "amount": salary_amt,
            "type": "Cr",
            "balance": current_balance
        })
    
    # Generate regular transactions
    remaining_trans = num_transactions - len(transactions)
    
    for _ in range(remaining_trans):
        tran_date = start_date + timedelta(days=random.randint(0, delta.days))
        tran_id = generate_transaction_id()
        
        # Transaction type distribution
        trans_type = random.choices(
            ['upi_merchant', 'upi_person', 'atm', 'neft', 'charges', 'interest'],
            weights=[45, 25, 10, 10, 5, 5]
        )[0]
        
        if trans_type == 'upi_merchant':
            merchant, upi_id, min_amt, max_amt = random.choice(UPI_MERCHANTS)
            amount = random.randint(min_amt, max_amt)
            current_balance -= amount
            description = f"UPIAR/{random.randint(100000000000, 999999999999)}/DR/{merchant}/{upi_id}"
            trans_type_flag = "Dr"
            
        elif trans_type == 'upi_person':
            if random.random() < 0.5:  # Credit from person
                person_name, upi_id = random.choice(PERSON_NAMES)
                amount = random.randint(500, 10000)
                current_balance += amount
                description = f"UPIAB/{random.randint(100000000000, 999999999999)}/CR/{person_name}/{upi_id}"
                trans_type_flag = "Cr"
            else:  # Debit to person
                person_name, upi_id = random.choice(PERSON_NAMES)
                amount = random.randint(500, 10000)
                current_balance -= amount
                description = f"UPIAR/{random.randint(100000000000, 999999999999)}/DR/{person_name}/{upi_id}"
                trans_type_flag = "Dr"
                
        elif trans_type == 'atm':
            amount = random.choice([500, 1000, 2000, 3000, 5000])
            current_balance -= amount
            description = f"ATM WDL {random.randint(100000, 999999)}\n{random.choice(['KANNUR', 'KASARAGOD', 'KOCHI'])}"
            trans_type_flag = "Dr"
            
        elif trans_type == 'neft':
            if random.random() < 0.3:  # NEFT Credit
                amount = random.randint(5000, 50000)
                current_balance += amount
                description = f"NEFT:CREDIT RECEIVED\nFDRLM{random.randint(8000000000, 8999999999)}"
                trans_type_flag = "Cr"
            else:  # NEFT Debit
                amount = random.randint(5000, 50000)
                current_balance -= amount
                description = f"NEFT:TRANSFER\nFDRLM{random.randint(8000000000, 8999999999)}"
                trans_type_flag = "Dr"
                
        elif trans_type == 'charges':
            charge_types = [
                ("SMS Charges", random.uniform(15, 20)),
                ("General Charges Recovery", random.uniform(100, 200)),
                ("MAND DR- BCF2442-", 2083.00)
            ]
            charge_name, amount = random.choice(charge_types)
            current_balance -= amount
            description = charge_name
            trans_type_flag = "Dr"
            
        else:  # interest
            amount = random.uniform(15, 50)
            current_balance += amount
            quarter_start = tran_date.replace(day=1, month=((tran_date.month-1)//3)*3+1)
            quarter_end = tran_date.replace(day=1)
            description = f"{transactions[0]['description'].split(':')[0] if transactions else 'Account'}:Int.Pd:{quarter_start.strftime('%d-%m-%Y')} to {quarter_end.strftime('%d-%m-%Y')}"
            trans_type_flag = "Cr"
        
        transactions.append({
            "tran_id": tran_id,
            "date": tran_date,
            "description": description,
            "amount": round(amount, 2),
            "type": trans_type_flag,
            "balance": round(current_balance, 2)
        })
    
    # Sort by date (newest first, like the original)
    transactions.sort(key=lambda x: x['date'], reverse=True)
    
    # Recalculate balances in reverse order to maintain logic
    final_balance = current_balance
    for i, trans in enumerate(transactions):
        if i == 0:
            trans['balance'] = final_balance
        else:
            prev_balance = transactions[i-1]['balance']
            if trans['type'] == 'Cr':
                trans['balance'] = prev_balance - trans['amount']
            else:
                trans['balance'] = prev_balance + trans['amount']
    
    return transactions, final_balance

def create_header_footer(canvas, doc):
    """Add header and footer to each page"""
    canvas.saveState()
    
    # Header - Union Bank Logo placeholder
    canvas.setFont('Helvetica-Bold', 14)
    canvas.drawString(30*mm, 285*mm, "UNION BANK OF INDIA")
    
    # Footer
    canvas.setFont('Helvetica', 8)
    canvas.drawString(30*mm, 10*mm, "This is system generated statement and does not require signature")
    canvas.drawString(30*mm, 7*mm, "https://www.unionbankofindia.co.in")
    
    # Page number
    page_num = canvas.getPageNumber()
    canvas.drawRightString(180*mm, 10*mm, f"Page {page_num}")
    
    canvas.restoreState()

def generate_union_bank_statement(customer, transactions, opening_balance, 
                                  statement_date, period_from, period_to, filename):
    """Generate a Union Bank statement PDF matching exact structure"""
    
    # Create PDF
    pdf = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=30*mm,
        bottomMargin=20*mm
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=12,
        textColor=colors.HexColor('#000080'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica-Bold',
        spaceAfter=3
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica',
        spaceAfter=3
    )
    
    small_style = ParagraphStyle(
        'SmallStyle',
        parent=styles['Normal'],
        fontSize=7,
        fontName='Helvetica'
    )
    
    # Build document content
    story = []
    
    # Title
    story.append(Paragraph("DETAILS OF STATEMENT", title_style))
    story.append(Spacer(1, 5*mm))
    
    # Customer Details Section
    details_data = [
        [Paragraph("<b>Name :</b>", normal_style), Paragraph(customer['name'], normal_style),
         Paragraph("<b>Home Branch :</b>", normal_style), Paragraph("CHERUVATHUR", normal_style)],
        [Paragraph("<b>Address :</b>", normal_style), Paragraph(customer['address_line1'], normal_style),
         Paragraph("<b>IFSC :</b>", normal_style), Paragraph(customer['ifsc'], normal_style)],
        ["", Paragraph(customer['address_line2'], normal_style),
         Paragraph("<b>Customer/CIF ID :</b>", normal_style), Paragraph(str(customer['cif_id']), normal_style)],
        ["", Paragraph(customer['address_line3'], normal_style),
         Paragraph("<b>Account Type :</b>", normal_style), Paragraph("Savings Account", normal_style)],
        [Paragraph("<b>City :</b>", normal_style), Paragraph(customer['city'], normal_style),
         Paragraph("<b>Account Number :</b>", normal_style), Paragraph(customer['account_number'], normal_style)],
        [Paragraph("<b>State :</b>", normal_style), Paragraph(customer['state'], normal_style),
         Paragraph("<b>Currency :</b>", normal_style), Paragraph("INR", normal_style)],
        [Paragraph("<b>Pincode :</b>", normal_style), Paragraph(str(customer['pincode']), normal_style),
         Paragraph("<b>Branch Address :</b>", normal_style), Paragraph("1st Floor, HI Lane Plaza, National", normal_style)],
        [Paragraph("<b>Mobile No :</b>", normal_style), Paragraph(customer['mobile'], normal_style),
         "", Paragraph("Highway, CHERUVATHUR, KASARAGOD", normal_style)],
        [Paragraph("<b>Email Id :</b>", normal_style), Paragraph(customer['email'], normal_style), "", ""],
    ]
    
    details_table = Table(details_data, colWidths=[30*mm, 50*mm, 40*mm, 50*mm])
    details_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))
    
    story.append(details_table)
    story.append(Spacer(1, 5*mm))
    
    # Statement Period
    period_data = [
        [Paragraph(f"<b>Statement Date :</b>{statement_date.strftime('%d/%m/%Y %I:%M %p')}", normal_style),
         Paragraph(f"<b>Statement Period From -</b>{period_from.strftime('%d/%m/%Y')} <b>To</b> {period_to.strftime('%d/%m/%Y')}", normal_style)]
    ]
    
    period_table = Table(period_data, colWidths=[85*mm, 85*mm])
    period_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#E8E8E8')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    
    story.append(period_table)
    story.append(Spacer(1, 3*mm))
    
    # Transaction Table Header
    trans_header = [
        [Paragraph("<b>Tran Id</b>", small_style),
         Paragraph("<b>Tran Date</b>", small_style),
         Paragraph("<b>Remarks</b>", small_style),
         Paragraph("<b>Amount (Rs.)</b>", small_style),
         Paragraph("<b>Balance (Rs.)</b>", small_style)]
    ]
    
    # Transaction rows
    trans_rows = []
    for trans in transactions:
        trans_rows.append([
            Paragraph(trans['tran_id'], small_style),
            Paragraph(trans['date'].strftime('%d/%m/%Y'), small_style),
            Paragraph(trans['description'].replace('\n', '<br/>'), small_style),
            Paragraph(f"{trans['amount']:.2f} ({trans['type']})", small_style),
            Paragraph(f"{trans['balance']:.2f}", small_style)
        ])
    
    # Split transactions across pages
    rows_per_page = 25
    for i in range(0, len(trans_rows), rows_per_page):
        page_rows = trans_header + trans_rows[i:i+rows_per_page]
        
        trans_table = Table(page_rows, colWidths=[25*mm, 20*mm, 75*mm, 25*mm, 25*mm])
        trans_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D3D3D3')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (3, 0), (4, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        
        story.append(trans_table)
        
        if i + rows_per_page < len(trans_rows):
            story.append(PageBreak())
    
    # Footer legends
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("<b>Statement Legends :</b>", normal_style))
    story.append(Paragraph("NEFT : National Electronic Fund Transfer &nbsp;&nbsp; UPI : Unified Payment Interface", small_style))
    story.append(Paragraph("RTGS : Real Time Gross Settlement &nbsp;&nbsp; INT : Intra Fund Transfer", small_style))
    story.append(Paragraph("BBPS : Bharat Bill Payment Service", small_style))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Request to our customers for notifying immediately, if there is any discrepancy in the statement.", small_style))
    story.append(Paragraph("Registered office: Union Bank Bhavan,239,Vidhan Bhavan Marg,Nariman Point,Mumbai-400021,India", small_style))
    
    # Build PDF
    pdf.build(story, onFirstPage=create_header_footer, onLaterPages=create_header_footer)
    print(f"✓ Generated: {filename}")

def main():
    """Main function to generate all statements"""
    
    # Create output directory - Go to BANKFUSION root, then raw_pdfs/union (NOT data/raw_pdfs)
    output_dir = "../../raw_pdfs/union"
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("Union Bank Statement Generator")
    print("=" * 60)
    
    # Generate 10 statements with 300 transactions
    print("\nGenerating 10 statements with 300 transactions each...")
    for i in range(1, 11):
        customer = generate_customer_details()
        
        # Random statement period (6 months)
        end_date = datetime(2024, random.randint(1, 12), random.randint(1, 28))
        start_date = end_date - timedelta(days=180)
        statement_date = end_date + timedelta(days=random.randint(1, 5))
        
        opening_balance = random.uniform(500, 15000)
        
        transactions, closing_balance = generate_transactions(
            300, start_date, end_date, opening_balance
        )
        
        filename = os.path.join(output_dir, f"Union_Statement_{i:02d}_300T.pdf")
        generate_union_bank_statement(
            customer, transactions, opening_balance,
            statement_date, start_date, end_date, filename
        )
    
    # Generate 10 statements with 150 transactions
    print("\nGenerating 10 statements with 150 transactions each...")
    for i in range(11, 21):
        customer = generate_customer_details()
        
        # Random statement period (3 months)
        end_date = datetime(2024, random.randint(1, 12), random.randint(1, 28))
        start_date = end_date - timedelta(days=90)
        statement_date = end_date + timedelta(days=random.randint(1, 5))
        
        opening_balance = random.uniform(1000, 20000)
        
        transactions, closing_balance = generate_transactions(
            150, start_date, end_date, opening_balance
        )
        
        filename = os.path.join(output_dir, f"Union_Statement_{i:02d}_150T.pdf")
        generate_union_bank_statement(
            customer, transactions, opening_balance,
            statement_date, start_date, end_date, filename
        )
    
    print("\n" + "=" * 60)
    print("✓ All 20 Union Bank statements generated successfully!")
    print(f"✓ Saved to: {output_dir}")
    print("=" * 60)

if __name__ == "__main__":
    main()