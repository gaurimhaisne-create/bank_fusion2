# backend/app.py
# backend/app.py
import json
from pathlib import Path
from flask import Flask, jsonify, request

from pdf_extractor.hdfc_extractor import HDFCExtractor
from pdf_extractor.axis_extractor import AxisExtractor
from pdf_extractor.sbi_extractor import SBIExtractor
from pdf_extractor.union_extractor import UnionExtractor
from pdf_extractor.boi_extractor import BOIExtractor
from pdf_extractor.central_extractor import CentralExtractor
from normalizer.transaction_normalizer import TransactionNormalizer

app = Flask(__name__)   # 👈 THIS IS WHAT GUNICORN NEEDS


class BankStatementProcessor:
    EXTRACTORS = {
        'hdfc': HDFCExtractor,
        'axis': AxisExtractor,
        'sbi': SBIExtractor,
        'union': UnionExtractor,
        'bank_of_india': BOIExtractor,
        'central': CentralExtractor,
        'central_bank': CentralExtractor
    }

    def __init__(self):
        project_root = Path(__file__).parent.parent
        self.raw_pdf_dir = project_root / 'data' / 'raw_pdfs'
        self.extracted_json_dir = project_root / 'data' / 'extracted_json'
        self.normalized_json_dir = project_root / 'data' / 'normalized_json'

    def process_all(self):
        if not self.raw_pdf_dir.exists():
            return {"error": "raw_pdfs directory not found"}

        results = []

        for bank_folder in self.raw_pdf_dir.iterdir():
            if not bank_folder.is_dir():
                continue

            bank_name = bank_folder.name.lower()
            extractor_class = self.EXTRACTORS.get(bank_name)
            if not extractor_class:
                continue

            for pdf_file in bank_folder.glob("*.pdf"):
                extractor = extractor_class(str(pdf_file))
                statement_data = extractor.extract()

                normalized = TransactionNormalizer.normalize_statement(statement_data)
                results.append({
                    "bank": bank_name,
                    "file": pdf_file.name,
                    "transactions": len(normalized)
                })

        return results


# ------------------ ROUTES ------------------

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "BankFusion backend running 🚀"})


@app.route("/process-all", methods=["POST"])
def process_all_route():
    processor = BankStatementProcessor()
    result = processor.process_all()
    return jsonify(result)


'''
import json
from pathlib import Path
from pdf_extractor.hdfc_extractor import HDFCExtractor
from pdf_extractor.axis_extractor import AxisExtractor
from pdf_extractor.sbi_extractor import SBIExtractor
from pdf_extractor.union_extractor import UnionExtractor
from pdf_extractor.boi_extractor import BOIExtractor
from pdf_extractor.central_extractor import CentralExtractor
from normalizer.transaction_normalizer import TransactionNormalizer


class BankStatementProcessor:
    EXTRACTORS = {
        'hdfc': HDFCExtractor,
        'axis': AxisExtractor,
        'sbi': SBIExtractor,
        'union': UnionExtractor,
        'bank_of_india': BOIExtractor,
        'central': CentralExtractor,
        'central_bank': CentralExtractor  # ADD THIS FOR CENTRAL_BANK FOLDER
    }

    def __init__(self, raw_pdf_dir: str = None,
                 extracted_json_dir: str = None,
                 normalized_json_dir: str = None):
        # Get the project root directory (parent of backend)
        project_root = Path(__file__).parent.parent
        
        self.raw_pdf_dir = Path(raw_pdf_dir) if raw_pdf_dir else project_root / 'data' / 'raw_pdfs'
        self.extracted_json_dir = Path(extracted_json_dir) if extracted_json_dir else project_root / 'data' / 'extracted_json'
        self.normalized_json_dir = Path(normalized_json_dir) if normalized_json_dir else project_root / 'data' / 'normalized_json'
        
        print(f"Looking for PDFs in: {self.raw_pdf_dir}")

    def process_all(self):
        # Check if directory exists
        if not self.raw_pdf_dir.exists():
            print(f"ERROR: Directory not found: {self.raw_pdf_dir}")
            print(f"Please create the directory and add PDF files.")
            return
            
        for bank_folder in self.raw_pdf_dir.iterdir():
            if not bank_folder.is_dir():
                continue

            bank_name = bank_folder.name.lower()
            print(f"\n{'='*60}")
            print(f"Processing {bank_name.upper()} statements...")
            print(f"{'='*60}")

            extractor_class = self.EXTRACTORS.get(bank_name)
            if not extractor_class:
                print(f"No extractor found for {bank_name}, skipping...")
                continue

            pdf_files = list(bank_folder.glob('*.pdf'))
            print(f"Found {len(pdf_files)} PDF files")

            if len(pdf_files) == 0:
                print(f"No PDF files found in {bank_folder}")
                continue

            for pdf_file in pdf_files:
                try:
                    print(f"\nProcessing: {pdf_file.name}")
                    
                    extractor = extractor_class(str(pdf_file))
                    statement_data = extractor.extract()
                    
                    extracted_output = self.extracted_json_dir / bank_name / f"{pdf_file.stem}.json"
                    extracted_output.parent.mkdir(parents=True, exist_ok=True)
                    with open(extracted_output, 'w') as f:
                        json.dump(statement_data, f, indent=2)
                    print(f"  ✓ Extracted: {extracted_output}")
                    
                    normalized_transactions = TransactionNormalizer.normalize_statement(statement_data)
                    
                    normalized_output = self.normalized_json_dir / f"{pdf_file.stem}_normalized.json"
                    normalized_output.parent.mkdir(parents=True, exist_ok=True)
                    with open(normalized_output, 'w') as f:
                        json.dump({
                            "bank_name": statement_data.get('bank_name', ''),
                            "account_number": statement_data.get('account_number', ''),
                            "account_holder": statement_data.get('account_holder', ''),
                            "statement_period": statement_data.get('statement_period', ''),
                            "transactions": normalized_transactions
                        }, f, indent=2)
                    print(f"  ✓ Normalized: {normalized_output}")
                    print(f"  ✓ Transactions: {len(normalized_transactions)}")
                    
                except Exception as e:
                    print(f"  ✗ Error processing {pdf_file.name}: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    continue

    def process_single(self, pdf_path: str, bank_name: str):
        extractor_class = self.EXTRACTORS.get(bank_name.lower())
        if not extractor_class:
            raise ValueError(f"Unknown bank: {bank_name}")

        pdf_file = Path(pdf_path)
        print(f"Processing: {pdf_file.name}")
        
        extractor = extractor_class(str(pdf_file))
        statement_data = extractor.extract()
        
        extracted_output = self.extracted_json_dir / bank_name.lower() / f"{pdf_file.stem}.json"
        extracted_output.parent.mkdir(parents=True, exist_ok=True)
        with open(extracted_output, 'w') as f:
            json.dump(statement_data, f, indent=2)
        print(f"Extracted: {extracted_output}")
        
        normalized_transactions = TransactionNormalizer.normalize_statement(statement_data)
        
        normalized_output = self.normalized_json_dir / f"{pdf_file.stem}_normalized.json"
        normalized_output.parent.mkdir(parents=True, exist_ok=True)
        with open(normalized_output, 'w') as f:
            json.dump({
                "bank_name": statement_data.get('bank_name', ''),
                "account_number": statement_data.get('account_number', ''),
                "account_holder": statement_data.get('account_holder', ''),
                "statement_period": statement_data.get('statement_period', ''),
                "transactions": normalized_transactions
            }, f, indent=2)
        print(f"Normalized: {normalized_output}")
        print(f"Transactions: {len(normalized_transactions)}")


if __name__ == "__main__":
    processor = BankStatementProcessor()
    processor.process_all()'''