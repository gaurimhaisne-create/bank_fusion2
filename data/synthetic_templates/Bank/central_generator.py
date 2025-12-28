import random
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import os

class BankStatementGenerator:
    def __init__(self):
        self.page_width, self.page_height = A4
        self.margin_left = 0.75 * inch
        self.margin_right = 0.5 * inch
        self.margin_top = 0.75 * inch
        self.margin_bottom = 0.5 * inch
        
        # Transaction categories with realistic merchants
        self.transaction_categories = {
            'food': [
                ('SWIGGY', (150, 800)),
                ('ZOMATO', (200, 900)),
                ('DOMINOS PIZZA', (300, 600)),
                ('MCDONALDS', (200, 500)),
                ('STARBUCKS', (150, 400)),
                ('SUBWAY', (150, 350)),
                ('KFC', (250, 550)),
                ('CAFE COFFEE DAY', (100, 300)),
                ('BARBEQUE NATION', (800, 1500)),
                ('HALDIRAMS', (150, 400))
            ],
            'groceries': [
                ('DMART', (500, 3000)),
                ('RELIANCE FRESH', (400, 2500)),
                ('BIG BAZAAR', (600, 3500)),
                ('MORE MEGASTORE', (300, 2000)),
                ('SPENCERS', (400, 2200)),
                ('LOCAL KIRANA', (200, 1500))
            ],
            'travel': [
                ('UBER', (80, 400)),
                ('OLA CABS', (70, 380)),
                ('INDIAN OIL PETROL', (500, 2500)),
                ('BHARAT PETROLEUM', (600, 2800)),
                ('METRO CARD RECHARGE', (200, 500)),
                ('IRCTC TRAIN BOOKING', (400, 2000)),
                ('MAKEMYTRIP', (2000, 15000)),
                ('GOIBIBO', (1500, 12000))
            ],
            'shopping': [
                ('AMAZON', (200, 5000)),
                ('FLIPKART', (300, 4500)),
                ('MYNTRA', (500, 3000)),
                ('AJIO', (400, 2500)),
                ('WESTSIDE', (800, 3500)),
                ('PANTALOONS', (600, 3000)),
                ('DECATHLON', (500, 4000))
            ],
            'entertainment': [
                ('NETFLIX', (199, 799)),
                ('AMAZON PRIME', (299, 1499)),
                ('HOTSTAR', (299, 1499)),
                ('BOOK MY SHOW', (200, 800)),
                ('PVR CINEMAS', (250, 1000)),
                ('INOX', (250, 950)),
                ('SPOTIFY', (119, 119)),
                ('YOUTUBE PREMIUM', (129, 129))
            ],
            'utilities': [
                ('ELECTRICITY BILL', (800, 3000)),
                ('MOBILE RECHARGE', (200, 800)),
                ('AIRTEL BROADBAND', (500, 1500)),
                ('JIO FIBER', (500, 1500)),
                ('DTH RECHARGE', (200, 600)),
                ('WATER BILL', (200, 800)),
                ('GAS CYLINDER', (800, 1000))
            ],
            'misc': [
                ('ATM CASH WITHDRAWAL', (500, 10000)),
                ('PHARMACY', (100, 1500)),
                ('BOOK STORE', (200, 1000)),
                ('SALON', (300, 1500)),
                ('GYM MEMBERSHIP', (1000, 3000)),
                ('RENT PAYMENT', (10000, 30000))
            ]
        }
        
        self.first_names = ['RAJESH', 'PRIYA', 'AMIT', 'SNEHA', 'VIKRAM', 'ANJALI', 
                           'RAHUL', 'POOJA', 'KARTHIK', 'DIVYA', 'SURESH', 'KAVITA',
                           'ARUN', 'MEERA', 'SANDEEP', 'NISHA', 'MANOJ', 'REKHA']
        self.last_names = ['KUMAR', 'SHARMA', 'PATEL', 'SINGH', 'REDDY', 'GUPTA',
                          'MEHTA', 'NAIR', 'IYER', 'VERMA', 'JOSHI', 'DESAI']
    
    def generate_account_number(self):
        return f"{random.randint(1000000000, 9999999999)}"
    
    def generate_customer_name(self):
        first = random.choice(self.first_names)
        last = random.choice(self.last_names)
        title = random.choice(['Mr.', 'Mrs.', 'Ms.'])
        return f"{title} {first} {last}"
    
    def generate_upi_rrn(self):
        return f"{random.randint(400000000000, 499999999999)}"
    
    def generate_transaction(self, date, balance):
        """Generate a realistic transaction"""
        category = random.choice(list(self.transaction_categories.keys()))
        merchant, amount_range = random.choice(self.transaction_categories[category])
        
        # Determine if debit or credit (90% debit, 10% credit)
        is_debit = random.random() < 0.9
        
        if is_debit:
            amount = round(random.uniform(amount_range[0], amount_range[1]), 2)
            new_balance = balance - amount
            txn_type = 'TO TRF.'
            description = f"UPI RRN {self.generate_upi_rrn()}\nTRF TO {merchant}"
        else:
            # Credits (salary, refunds, transfers)
            credit_types = [
                ('SALARY CREDIT', (30000, 80000)),
                ('REFUND', (100, 2000)),
                ('TRF FROM FRIEND', (500, 5000))
            ]
            credit_desc, credit_range = random.choice(credit_types)
            amount = round(random.uniform(credit_range[0], credit_range[1]), 2)
            new_balance = balance + amount
            txn_type = 'BY TRF.'
            description = f"UPI RRN {self.generate_upi_rrn()}\n{credit_desc}"
        
        return {
            'date': date,
            'type': txn_type,
            'description': description,
            'debit': amount if is_debit else 0,
            'credit': amount if not is_debit else 0,
            'balance': new_balance
        }
    
    def generate_transactions(self, num_transactions, start_date, end_date, opening_balance):
        """Generate a list of transactions with proper date distribution"""
        transactions = []
        current_balance = opening_balance
        
        # Generate random dates within the period
        date_range = (end_date - start_date).days
        transaction_dates = sorted([
            start_date + timedelta(days=random.randint(0, date_range))
            for _ in range(num_transactions)
        ])
        
        for txn_date in transaction_dates:
            txn = self.generate_transaction(txn_date, current_balance)
            current_balance = txn['balance']
            transactions.append(txn)
        
        return transactions, current_balance
    
    def draw_bank_logo(self, c):
        """Draw bank logo and name"""
        y = self.page_height - 50
        
        # Bank name
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(self.page_width / 2, y, "Central Bank")
        y -= 18
        c.setFont("Helvetica-Oblique", 12)
        c.drawCentredString(self.page_width / 2, y, "of India")
        
        return y - 30
    
    def draw_header(self, c, page_num, customer_name, account_no):
        """Draw the statement header"""
        y = self.draw_bank_logo(c)
        
        y -= 20
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(self.page_width / 2, y, "STATEMENT OF ACCOUNT")
        
        y -= 25
        c.setFont("Helvetica", 10)
        
        # Customer name on left, Account details on right
        c.drawString(self.margin_left, y, f"{customer_name}")
        
        # Account number and page number aligned to right
        account_text = f"Account No. : {account_no}"
        page_text = f"Page No. : {page_num}"
        
        c.drawString(self.page_width - self.margin_right - 220, y, account_text)
        c.drawString(self.page_width - self.margin_right - 80, y, page_text)
        
        y -= 15
        c.line(self.margin_left, y, self.page_width - self.margin_right, y)
        
        return y - 15
    
    def draw_transaction_table_header(self, c, y):
        """Draw the transaction table header"""
        c.setFont("Helvetica-Bold", 9)
        
        # Adjusted column positions with proper spacing - everything fits in page
        col_positions = {
            'value_date': self.margin_left,
            'post_date': self.margin_left + 60,
            'details': self.margin_left + 125,
            'chq_no': self.margin_left + 310,
            'debit': self.margin_left + 355,
            'credit': self.margin_left + 415,
            'balance': self.margin_left + 475
        }
        
        # First row of headers
        c.drawString(col_positions['value_date'], y, "Value")
        c.drawString(col_positions['post_date'], y, "Post")
        c.drawString(col_positions['details'], y, "Details")
        c.drawString(col_positions['chq_no'], y, "Chq.No.")
        c.drawString(col_positions['debit'], y, "Debit")
        c.drawString(col_positions['credit'], y, "Credit")
        c.drawString(col_positions['balance'], y, "Balance")
        
        y -= 12
        # Second row
        c.drawString(col_positions['value_date'], y, "Date")
        c.drawString(col_positions['post_date'], y, "Date")
        
        y -= 10
        c.line(self.margin_left, y, self.page_width - self.margin_right, y)
        
        return y - 10, col_positions
    
    def draw_transaction(self, c, y, txn, col_positions, is_brought_forward=False, balance_only=False):
        """Draw a single transaction row"""
        c.setFont("Helvetica", 8)
        
        if is_brought_forward:
            c.drawString(col_positions['details'], y, "BROUGHT FORWARD :")
            c.drawRightString(col_positions['balance'] + 50, y, f"{txn['balance']:,.2f}Cr")
            return y - 12
        
        if balance_only:
            c.drawString(col_positions['details'], y, "CARRIED FORWARD :")
            c.drawRightString(col_positions['balance'] + 50, y, f"{txn['balance']:,.2f}Cr")
            return y - 12
        
        # Date
        date_str = txn['date'].strftime('%d/%m/%y')
        c.drawString(col_positions['value_date'], y, date_str)
        c.drawString(col_positions['post_date'], y, date_str)
        
        # Transaction type and description
        lines = [txn['type']] + txn['description'].split('\n')
        c.drawString(col_positions['details'], y, lines[0])
        
        # Chq.No column (empty with dash)
        c.drawString(col_positions['chq_no'], y, "-")
        
        # Amounts - right aligned with reduced width
        if txn['debit'] > 0:
            c.drawRightString(col_positions['debit'] + 45, y, f"{txn['debit']:,.2f}")
        if txn['credit'] > 0:
            c.drawRightString(col_positions['credit'] + 45, y, f"{txn['credit']:,.2f}")
        
        # Balance - right aligned with Cr suffix - fits within page
        c.drawRightString(col_positions['balance'] + 50, y, f"{txn['balance']:,.2f}Cr")
        
        y -= 10
        
        # Additional description lines (indented slightly)
        for line in lines[1:]:
            c.drawString(col_positions['details'] + 5, y, line)
            c.drawString(col_positions['chq_no'], y, ".")
            y -= 10
        
        return y - 2
    
    def draw_footer(self, c, y, total_debit, total_credit, debit_count, credit_count):
        """Draw page footer with summary"""
        y -= 5
        c.line(self.margin_left, y, self.page_width - self.margin_right, y)
        y -= 15
        
        c.setFont("Helvetica", 8)
        summary = f"Page Summary Dr. Count {debit_count}  Cr. Count {credit_count}  {total_debit:,.2f}  {total_credit:,.2f}"
        c.drawString(self.margin_left, y, summary)
        
        y -= 15
        c.setFont("Helvetica", 7)
        c.drawString(self.margin_left, y, "Toll Free No. 18003030")
        
        y -= 10
        c.drawString(self.margin_left, y, "This is system generated statement hence signature or seal is not required")
    
    def generate_pdf(self, filename, num_transactions):
        """Generate a complete bank statement PDF"""
        c = canvas.Canvas(filename, pagesize=A4)
        
        # Generate statement data
        customer_name = self.generate_customer_name()
        account_no = self.generate_account_number()
        
        # Random statement period (last 1-3 months)
        end_date = datetime.now() - timedelta(days=random.randint(1, 30))
        start_date = end_date - timedelta(days=random.randint(28, 45))
        
        opening_balance = round(random.uniform(50000, 500000), 2)
        
        transactions, closing_balance = self.generate_transactions(
            num_transactions, start_date, end_date, opening_balance
        )
        
        # Add opening balance as first entry
        all_entries = [{'date': start_date, 'balance': opening_balance, 'type': 'opening'}] + transactions
        
        # Generate pages
        page_num = 1
        entries_per_page = 20  # More transactions per page
        
        # Track overall totals for final footer
        total_debit = sum(t['debit'] for t in transactions)
        total_credit = sum(t['credit'] for t in transactions)
        total_debit_count = sum(1 for t in transactions if t['debit'] > 0)
        total_credit_count = sum(1 for t in transactions if t['credit'] > 0)
        
        for i in range(0, len(all_entries), entries_per_page):
            page_entries = all_entries[i:i + entries_per_page]
            
            y = self.draw_header(c, page_num, customer_name, account_no)
            y, col_positions = self.draw_transaction_table_header(c, y)
            
            # First entry on page
            if i == 0:
                y = self.draw_transaction(c, y, page_entries[0], col_positions, is_brought_forward=True)
                page_entries = page_entries[1:]
            else:
                brought_forward = {'balance': all_entries[i-1]['balance']}
                y = self.draw_transaction(c, y, brought_forward, col_positions, is_brought_forward=True)
            
            # Draw transactions
            for entry in page_entries:
                if y < 120:  # Need new page
                    carried_forward = {'balance': entry['balance']}
                    y = self.draw_transaction(c, y + 12, carried_forward, col_positions, balance_only=True)
                    # No footer on intermediate pages
                    c.showPage()
                    page_num += 1
                    y = self.draw_header(c, page_num, customer_name, account_no)
                    y, col_positions = self.draw_transaction_table_header(c, y)
                    y = self.draw_transaction(c, y, carried_forward, col_positions, is_brought_forward=True)
                
                if entry.get('type') != 'opening':
                    y = self.draw_transaction(c, y, entry, col_positions)
            
            # Check if this is the last page
            if i + entries_per_page >= len(all_entries):
                # Add carried forward and footer only on the last page
                carried_forward = {'balance': closing_balance}
                y = self.draw_transaction(c, y, carried_forward, col_positions, balance_only=True)
                self.draw_footer(c, y, total_debit, total_credit, total_debit_count, total_credit_count)
            else:
                # Just add new page without footer
                c.showPage()
                page_num += 1
        
        c.save()
        print(f"✓ Generated: {os.path.basename(filename)} ({num_transactions} txns, {page_num} pages)")

def main():
    """Generate all bank statement PDFs"""
    generator = BankStatementGenerator()
    
    # FIXED: Go up 3 levels from synthetic_templates/Bank/ to BANKFUSION root
    # Then navigate to data/raw_pdfs/Central_Bank/
    output_dir = "../../../data/raw_pdfs/Central"
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 70)
    print("Central Bank Statement Generator")
    print("=" * 70)
    print(f"📁 Output Directory: {os.path.abspath(output_dir)}")
    print("=" * 70)
    
    # Generate 10 PDFs with 300 transactions
    print("\n📊 Generating 10 statements with 300 transactions each...")
    for i in range(1, 11):
        filename = os.path.join(output_dir, f"Statement_{i:02d}_300txn.pdf")
        generator.generate_pdf(filename, 300)
    
    # Generate 10 PDFs with 150 transactions
    print("\n📊 Generating 10 statements with 150 transactions each...")
    for i in range(11, 21):
        filename = os.path.join(output_dir, f"Statement_{i:02d}_150txn.pdf")
        generator.generate_pdf(filename, 150)
    
    print("\n" + "=" * 70)
    print("✅ SUCCESS! Generated 20 bank statement PDFs")
    print("   • 10 PDFs with 300 transactions")
    print("   • 10 PDFs with 150 transactions")
    print("=" * 70)

if __name__ == "__main__":
    main()