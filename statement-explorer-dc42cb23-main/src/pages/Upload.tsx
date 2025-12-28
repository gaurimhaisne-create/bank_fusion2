import { useState, useCallback } from "react";
import { Upload as UploadIcon, FileText, CheckCircle, AlertCircle, Download, Loader2, X } from "lucide-react";
import { useNavigate } from "react-router-dom";
import Header from "@/components/Header";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";
import { useToast } from "@/hooks/use-toast";
import { useTransactions, Transaction, BankStatement } from "@/context/TransactionContext";

interface UploadedFile {
  name: string;
  size: number;
  status: "uploading" | "processing" | "success" | "error";
  progress: number;
  error?: string;
  statementData?: BankStatement;
}

const formatINR = (amount: number) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 2,
  }).format(amount);
};

const Upload = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const navigate = useNavigate();
  const { toast } = useToast();
  const { addStatement, statements } = useTransactions();

  const generateMockTransactions = (): Transaction[] => {
    const categories = ["Groceries", "Utilities", "Entertainment", "Shopping", "Transport", "Food", "Healthcare", "Income"];
    const descriptions: Record<string, string[]> = {
      Income: ["Salary Deposit", "Freelance Payment", "Interest Credit", "Bonus", "Refund"],
      Groceries: ["Big Bazaar", "DMart", "Reliance Fresh", "More Supermarket", "Spencer's"],
      Utilities: ["Electricity Bill", "Water Bill", "Gas Bill", "Internet Bill", "Mobile Recharge"],
      Entertainment: ["Netflix", "Amazon Prime", "Movie Tickets", "Concert Tickets", "Gaming"],
      Shopping: ["Amazon", "Flipkart", "Myntra", "Ajio", "Local Market"],
      Transport: ["Uber", "Ola", "Petrol", "Metro Card", "Bus Pass"],
      Food: ["Swiggy", "Zomato", "Restaurant", "Cafe Coffee Day", "Dominos"],
      Healthcare: ["Apollo Pharmacy", "Hospital Visit", "Lab Tests", "Medicine", "Insurance Premium"],
    };

    const transactions: Transaction[] = [];
    const numTransactions = 15 + Math.floor(Math.random() * 10);

    // Add income transactions first
    const incomeCount = 2 + Math.floor(Math.random() * 3);
    for (let i = 0; i < incomeCount; i++) {
      const incomeDesc = descriptions.Income[Math.floor(Math.random() * descriptions.Income.length)];
      const incomeAmount = 15000 + Math.floor(Math.random() * 35000);
      const day = 1 + Math.floor(Math.random() * 28);
      transactions.push({
        id: `txn-${Date.now()}-${i}`,
        date: `2024-01-${day.toString().padStart(2, '0')}`,
        description: incomeDesc,
        category: "Income",
        amount: incomeAmount,
        type: "Income",
      });
    }

    // Add expense transactions
    const expenseCategories = categories.filter(c => c !== "Income");
    for (let i = incomeCount; i < numTransactions; i++) {
      const category = expenseCategories[Math.floor(Math.random() * expenseCategories.length)];
      const desc = descriptions[category][Math.floor(Math.random() * descriptions[category].length)];
      const day = 1 + Math.floor(Math.random() * 28);
      
      let amount: number;
      if (category === "Utilities") {
        amount = -(500 + Math.floor(Math.random() * 2500));
      } else if (category === "Groceries") {
        amount = -(200 + Math.floor(Math.random() * 3000));
      } else if (category === "Healthcare") {
        amount = -(500 + Math.floor(Math.random() * 5000));
      } else if (category === "Entertainment") {
        amount = -(100 + Math.floor(Math.random() * 1500));
      } else {
        amount = -(100 + Math.floor(Math.random() * 2000));
      }

      transactions.push({
        id: `txn-${Date.now()}-${i}`,
        date: `2024-01-${day.toString().padStart(2, '0')}`,
        description: desc,
        category,
        amount,
        type: "Expense",
      });
    }

    // Sort by date
    return transactions.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
  };

  const simulateProcessing = (file: File) => {
    const uploadedFile: UploadedFile = {
      name: file.name,
      size: file.size,
      status: "uploading",
      progress: 0,
    };

    setFiles((prev) => [...prev, uploadedFile]);

    let progress = 0;
    const uploadInterval = setInterval(() => {
      progress += Math.random() * 30;
      if (progress >= 100) {
        progress = 100;
        clearInterval(uploadInterval);
        
        setFiles((prev) =>
          prev.map((f) =>
            f.name === file.name ? { ...f, status: "processing", progress: 100 } : f
          )
        );

        setTimeout(() => {
          const transactions = generateMockTransactions();
          const totalCredits = transactions.filter(t => t.type === "Income").reduce((sum, t) => sum + t.amount, 0);
          const totalDebits = transactions.filter(t => t.type === "Expense").reduce((sum, t) => sum + Math.abs(t.amount), 0);
          const openingBalance = 5000 + Math.floor(Math.random() * 10000);
          
          const statementData: BankStatement = {
            fileName: file.name,
            accountHolder: "Account Holder",
            accountNumber: `****${Math.floor(1000 + Math.random() * 9000)}`,
            statementPeriod: "Jan 1, 2024 - Jan 31, 2024",
            openingBalance,
            closingBalance: openingBalance + totalCredits - totalDebits,
            totalCredits,
            totalDebits,
            transactions,
            uploadedAt: new Date().toISOString(),
          };

          // Add to global context
          addStatement(statementData);

          setFiles((prev) =>
            prev.map((f) =>
              f.name === file.name ? { ...f, status: "success", statementData } : f
            )
          );

          toast({
            title: "Processing Complete",
            description: `${file.name} has been successfully processed with ${transactions.length} transactions.`,
          });
        }, 2000);
      } else {
        setFiles((prev) =>
          prev.map((f) =>
            f.name === file.name ? { ...f, progress } : f
          )
        );
      }
    }, 200);
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const droppedFiles = Array.from(e.dataTransfer.files);
    const pdfFiles = droppedFiles.filter((f) => f.type === "application/pdf");

    if (pdfFiles.length === 0) {
      toast({
        title: "Invalid File Type",
        description: "Please upload PDF files only.",
        variant: "destructive",
      });
      return;
    }

    pdfFiles.forEach(simulateProcessing);
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || []);
    const pdfFiles = selectedFiles.filter((f) => f.type === "application/pdf");

    if (pdfFiles.length === 0) {
      toast({
        title: "Invalid File Type",
        description: "Please upload PDF files only.",
        variant: "destructive",
      });
      return;
    }

    pdfFiles.forEach(simulateProcessing);
  };

  const downloadJSON = (file: UploadedFile) => {
    if (file.statementData) {
      const exportData = {
        meta: {
          exportedAt: new Date().toISOString(),
          fileName: file.statementData.fileName,
          currency: "INR",
        },
        accountInfo: {
          holder: file.statementData.accountHolder,
          number: file.statementData.accountNumber,
          period: file.statementData.statementPeriod,
        },
        summary: {
          openingBalance: file.statementData.openingBalance,
          closingBalance: file.statementData.closingBalance,
          totalIncome: file.statementData.totalCredits,
          totalExpenses: file.statementData.totalDebits,
          netFlow: file.statementData.totalCredits - file.statementData.totalDebits,
          transactionCount: file.statementData.transactions.length,
          formattedSummary: {
            openingBalance: formatINR(file.statementData.openingBalance),
            closingBalance: formatINR(file.statementData.closingBalance),
            totalIncome: formatINR(file.statementData.totalCredits),
            totalExpenses: formatINR(file.statementData.totalDebits),
            netFlow: formatINR(file.statementData.totalCredits - file.statementData.totalDebits),
          }
        },
        transactions: file.statementData.transactions.map((t, index) => ({
          transactionId: t.id,
          serialNumber: index + 1,
          date: t.date,
          description: t.description,
          category: t.category,
          type: t.type,
          amount: {
            value: t.amount,
            absolute: Math.abs(t.amount),
            formatted: formatINR(Math.abs(t.amount)),
            currency: "INR",
          },
          metadata: {
            isCredit: t.type === "Income",
            isDebit: t.type === "Expense",
          }
        })),
        categoryBreakdown: getCategoryBreakdown(file.statementData.transactions),
      };

      const dataStr = JSON.stringify(exportData, null, 2);
      const blob = new Blob([dataStr], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `${file.name.replace(".pdf", "")}_complete_export.json`;
      link.click();
      URL.revokeObjectURL(url);
    }
  };

  const getCategoryBreakdown = (transactions: Transaction[]) => {
    const breakdown: Record<string, { count: number; total: number; formatted: string }> = {};
    transactions.forEach((t) => {
      if (!breakdown[t.category]) {
        breakdown[t.category] = { count: 0, total: 0, formatted: "" };
      }
      breakdown[t.category].count += 1;
      breakdown[t.category].total += Math.abs(t.amount);
    });
    Object.keys(breakdown).forEach((key) => {
      breakdown[key].formatted = formatINR(breakdown[key].total);
    });
    return breakdown;
  };

  const removeFile = (fileName: string) => {
    setFiles((prev) => prev.filter((f) => f.name !== fileName));
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
  };

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container py-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-foreground">Upload Bank Statement</h1>
          <p className="text-muted-foreground">Upload your PDF bank statements to extract transaction data</p>
          {statements.length > 0 && (
            <p className="text-sm text-income mt-2">
              ✓ {statements.length} statement(s) loaded with {statements.reduce((sum, s) => sum + s.transactions.length, 0)} transactions
            </p>
          )}
        </div>

        {/* Upload Zone */}
        <div
          className={cn(
            "upload-zone cursor-pointer mb-8",
            isDragging && "dragging"
          )}
          onDragOver={(e) => {
            e.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
          onClick={() => document.getElementById("file-input")?.click()}
        >
          <input
            id="file-input"
            type="file"
            accept=".pdf"
            multiple
            className="hidden"
            onChange={handleFileSelect}
          />
          <div className="flex flex-col items-center gap-4">
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
              <UploadIcon className="h-8 w-8 text-primary" />
            </div>
            <div>
              <p className="text-lg font-medium text-foreground">
                Drop your PDF files here or click to browse
              </p>
              <p className="text-sm text-muted-foreground mt-1">
                Supports PDF bank statements up to 10MB
              </p>
            </div>
            <Button variant="outline" className="mt-2">
              Select Files
            </Button>
          </div>
        </div>

        {/* File List */}
        {files.length > 0 && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-foreground">Uploaded Files</h2>
            <div className="space-y-3">
              {files.map((file) => (
                <div
                  key={file.name}
                  className="rounded-xl border border-border bg-card p-4 shadow-sm animate-fade-in"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-expense/10">
                        <FileText className="h-5 w-5 text-expense" />
                      </div>
                      <div>
                        <p className="font-medium text-foreground">{file.name}</p>
                        <p className="text-sm text-muted-foreground">
                          {formatFileSize(file.size)}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      {file.status === "uploading" && (
                        <div className="flex items-center gap-2 text-muted-foreground">
                          <Loader2 className="h-4 w-4 animate-spin" />
                          <span className="text-sm">Uploading...</span>
                        </div>
                      )}
                      {file.status === "processing" && (
                        <div className="flex items-center gap-2 text-warning">
                          <Loader2 className="h-4 w-4 animate-spin" />
                          <span className="text-sm">Processing...</span>
                        </div>
                      )}
                      {file.status === "success" && (
                        <div className="flex items-center gap-2">
                          <CheckCircle className="h-5 w-5 text-income" />
                          <span className="text-sm text-income font-medium">
                            {file.statementData?.transactions.length} transactions
                          </span>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={(e) => {
                              e.stopPropagation();
                              downloadJSON(file);
                            }}
                            className="ml-2 gap-1"
                          >
                            <Download className="h-4 w-4" />
                            Export JSON
                          </Button>
                        </div>
                      )}
                      {file.status === "error" && (
                        <div className="flex items-center gap-2 text-expense">
                          <AlertCircle className="h-5 w-5" />
                          <span className="text-sm">{file.error || "Error"}</span>
                        </div>
                      )}
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          removeFile(file.name);
                        }}
                        className="ml-2 text-muted-foreground hover:text-foreground"
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                  {(file.status === "uploading" || file.status === "processing") && (
                    <Progress value={file.progress} className="mt-3 h-2" />
                  )}
                  
                  {/* Summary Preview */}
                  {file.status === "success" && file.statementData && (
                    <div className="mt-4 rounded-lg bg-muted/50 p-4">
                      <p className="text-sm font-medium text-foreground mb-3">Statement Summary:</p>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div>
                          <p className="text-muted-foreground">Account</p>
                          <p className="font-medium">{file.statementData.accountNumber}</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Total Income</p>
                          <p className="font-medium text-income">{formatINR(file.statementData.totalCredits)}</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Total Expenses</p>
                          <p className="font-medium text-expense">{formatINR(file.statementData.totalDebits)}</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Net Balance</p>
                          <p className={cn(
                            "font-medium",
                            file.statementData.totalCredits - file.statementData.totalDebits >= 0 ? "text-income" : "text-expense"
                          )}>
                            {formatINR(file.statementData.totalCredits - file.statementData.totalDebits)}
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {files.some((f) => f.status === "success") && (
              <div className="flex gap-3 pt-4">
                <Button onClick={() => navigate("/dashboard")} className="gap-2">
                  View Dashboard
                </Button>
                <Button variant="outline" onClick={() => navigate("/transactions")} className="gap-2">
                  View Transactions
                </Button>
              </div>
            )}
          </div>
        )}

        {/* Features */}
        <div className="mt-12 grid gap-6 sm:grid-cols-3">
          <div className="rounded-xl border border-border bg-card p-6 text-center">
            <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
              <FileText className="h-6 w-6 text-primary" />
            </div>
            <h3 className="font-semibold text-foreground">PDF Parsing</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              Automatically extract transaction data from your bank statement PDFs
            </p>
          </div>
          <div className="rounded-xl border border-border bg-card p-6 text-center">
            <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-income/10">
              <CheckCircle className="h-6 w-6 text-income" />
            </div>
            <h3 className="font-semibold text-foreground">Data Validation</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              Intelligent validation ensures accurate transaction categorization
            </p>
          </div>
          <div className="rounded-xl border border-border bg-card p-6 text-center">
            <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-chart-2/10">
              <Download className="h-6 w-6 text-chart-2" />
            </div>
            <h3 className="font-semibold text-foreground">JSON Export</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              Download complete structured JSON with all transaction details
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Upload;
