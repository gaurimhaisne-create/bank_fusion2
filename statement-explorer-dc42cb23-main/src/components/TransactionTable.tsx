import { useState, useMemo } from "react";
import { Search, Filter, ArrowUpDown, Download, Code2, Table2, Eye, Sparkles, TrendingUp, TrendingDown } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { cn } from "@/lib/utils";

export interface Transaction {
  id: string;
  date: string;
  description: string;
  category: string;
  type: "Income" | "Expense";
  amount: number;
}

export interface NormalizedTransaction {
  transaction_id: string;
  timestamp: string;
  iso_date: string;
  merchant: {
    name: string;
    category: string;
    category_code: string;
  };
  amount: {
    value: number;
    currency: string;
    formatted: string;
  };
  transaction_type: "CREDIT" | "DEBIT";
  status: "COMPLETED";
  metadata: {
    source: string;
    extracted_at: string;
    confidence_score: number;
  };
}

const defaultTransactions: Transaction[] = [
  { id: "1", date: "Feb 3, 2024", description: "PVR Cinemas", category: "Entertainment", type: "Expense", amount: -850.00 },
  { id: "2", date: "Feb 2, 2024", description: "Apollo Pharmacy", category: "Health & Fitness", type: "Expense", amount: -1249.00 },
  { id: "3", date: "Feb 1, 2024", description: "Rent Payment", category: "Housing", type: "Expense", amount: -35000.00 },
  { id: "4", date: "Jan 31, 2024", description: "Mutual Fund Returns", category: "Income", type: "Income", amount: 8500.00 },
  { id: "5", date: "Jan 30, 2024", description: "Big Bazaar", category: "Groceries", type: "Expense", amount: -3245.00 },
  { id: "6", date: "Jan 29, 2024", description: "Jio Fiber Bill", category: "Utilities", type: "Expense", amount: -999.00 },
  { id: "7", date: "Jan 28, 2024", description: "Zomato Order", category: "Food & Dining", type: "Expense", amount: -456.00 },
  { id: "8", date: "Jan 27, 2024", description: "BWSSB Water Bill", category: "Utilities", type: "Expense", amount: -650.00 },
  { id: "9", date: "Jan 26, 2024", description: "Myntra Shopping", category: "Shopping", type: "Expense", amount: -2899.00 },
  { id: "10", date: "Jan 25, 2024", description: "Spotify Premium", category: "Entertainment", type: "Expense", amount: -119.00 },
  { id: "11", date: "Jan 24, 2024", description: "Ola Ride", category: "Transportation", type: "Expense", amount: -345.00 },
  { id: "12", date: "Jan 23, 2024", description: "Cult Fit Membership", category: "Health & Fitness", type: "Expense", amount: -1499.00 },
  { id: "13", date: "Jan 22, 2024", description: "Salary Credit", category: "Income", type: "Income", amount: 125000.00 },
  { id: "14", date: "Jan 21, 2024", description: "BESCOM Electricity", category: "Utilities", type: "Expense", amount: -2800.00 },
  { id: "15", date: "Jan 20, 2024", description: "Amazon India", category: "Shopping", type: "Expense", amount: -4599.00 },
];

const categories = [
  "All Categories",
  "Entertainment",
  "Health & Fitness",
  "Housing",
  "Income",
  "Groceries",
  "Utilities",
  "Food & Dining",
  "Shopping",
  "Transportation",
];

const categoryColors: Record<string, string> = {
  "Entertainment": "bg-purple-500/10 text-purple-600 border-purple-500/20",
  "Health & Fitness": "bg-pink-500/10 text-pink-600 border-pink-500/20",
  "Housing": "bg-blue-500/10 text-blue-600 border-blue-500/20",
  "Income": "bg-emerald-500/10 text-emerald-600 border-emerald-500/20",
  "Groceries": "bg-orange-500/10 text-orange-600 border-orange-500/20",
  "Utilities": "bg-cyan-500/10 text-cyan-600 border-cyan-500/20",
  "Food & Dining": "bg-amber-500/10 text-amber-600 border-amber-500/20",
  "Shopping": "bg-rose-500/10 text-rose-600 border-rose-500/20",
  "Transportation": "bg-indigo-500/10 text-indigo-600 border-indigo-500/20",
};

const categoryIcons: Record<string, string> = {
  "Entertainment": "🎬",
  "Health & Fitness": "💪",
  "Housing": "🏠",
  "Income": "💰",
  "Groceries": "🛒",
  "Utilities": "⚡",
  "Food & Dining": "🍕",
  "Shopping": "🛍️",
  "Transportation": "🚗",
};

interface TransactionTableProps {
  transactions?: Transaction[];
  onDownloadJSON?: () => void;
}

const formatINR = (amount: number): string => {
  const absAmount = Math.abs(amount);
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(absAmount);
};

const normalizeTransaction = (t: Transaction): NormalizedTransaction => {
  const date = new Date(t.date);
  return {
    transaction_id: `TXN${t.id.padStart(8, '0')}`,
    timestamp: date.toISOString(),
    iso_date: date.toISOString().split('T')[0],
    merchant: {
      name: t.description,
      category: t.category,
      category_code: t.category.toUpperCase().replace(/[^A-Z]/g, '_'),
    },
    amount: {
      value: Math.abs(t.amount),
      currency: "INR",
      formatted: formatINR(t.amount),
    },
    transaction_type: t.type === "Income" ? "CREDIT" : "DEBIT",
    status: "COMPLETED",
    metadata: {
      source: "bank_statement_ocr",
      extracted_at: new Date().toISOString(),
      confidence_score: 0.95 + Math.random() * 0.05,
    },
  };
};

const TransactionTable = ({ transactions = defaultTransactions, onDownloadJSON }: TransactionTableProps) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All Categories");
  const [sortField, setSortField] = useState<keyof Transaction>("date");
  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("desc");
  const [hoveredRow, setHoveredRow] = useState<string | null>(null);
  const [selectedTransaction, setSelectedTransaction] = useState<Transaction | null>(null);

  const filteredTransactions = useMemo(() => {
    return transactions
      .filter((t) => {
        const matchesSearch = t.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
          t.category.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesCategory = selectedCategory === "All Categories" || t.category === selectedCategory;
        return matchesSearch && matchesCategory;
      })
      .sort((a, b) => {
        if (sortField === "amount") {
          return sortDirection === "asc" ? a.amount - b.amount : b.amount - a.amount;
        }
        if (sortField === "date") {
          return sortDirection === "asc" 
            ? new Date(a.date).getTime() - new Date(b.date).getTime()
            : new Date(b.date).getTime() - new Date(a.date).getTime();
        }
        return 0;
      });
  }, [transactions, searchQuery, selectedCategory, sortField, sortDirection]);

  const normalizedData = useMemo(() => {
    return {
      schema_version: "1.0.0",
      bank_statement: {
        account_holder: "Account Holder",
        account_number: "XXXX XXXX 1234",
        bank_name: "Sample Bank",
        statement_period: {
          from: "2024-01-20",
          to: "2024-02-03",
        },
      },
      summary: {
        total_transactions: filteredTransactions.length,
        total_credits: filteredTransactions.filter(t => t.type === "Income").reduce((sum, t) => sum + t.amount, 0),
        total_debits: Math.abs(filteredTransactions.filter(t => t.type === "Expense").reduce((sum, t) => sum + t.amount, 0)),
        currency: "INR",
      },
      transactions: filteredTransactions.map(normalizeTransaction),
    };
  }, [filteredTransactions]);

  const handleSort = (field: keyof Transaction) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("desc");
    }
  };

  const handleDownload = (type: "raw" | "normalized") => {
    const data = type === "normalized" ? normalizedData : filteredTransactions;
    const dataStr = JSON.stringify(data, null, 2);
    const blob = new Blob([dataStr], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = type === "normalized" ? "normalized_transactions.json" : "transactions.json";
    link.click();
    URL.revokeObjectURL(url);
  };

  const totalIncome = filteredTransactions.filter(t => t.type === "Income").reduce((sum, t) => sum + t.amount, 0);
  const totalExpense = Math.abs(filteredTransactions.filter(t => t.type === "Expense").reduce((sum, t) => sum + t.amount, 0));

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="relative overflow-hidden rounded-xl bg-gradient-to-br from-emerald-500/10 via-emerald-500/5 to-transparent border border-emerald-500/20 p-4 group hover:border-emerald-500/40 transition-all duration-300">
          <div className="absolute top-0 right-0 w-20 h-20 bg-emerald-500/10 rounded-full blur-2xl group-hover:scale-150 transition-transform duration-500" />
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-emerald-500/20">
              <TrendingUp className="h-5 w-5 text-emerald-600" />
            </div>
            <div>
              <p className="text-xs text-muted-foreground font-medium">Total Income</p>
              <p className="text-xl font-bold text-emerald-600">{formatINR(totalIncome)}</p>
            </div>
          </div>
        </div>
        <div className="relative overflow-hidden rounded-xl bg-gradient-to-br from-rose-500/10 via-rose-500/5 to-transparent border border-rose-500/20 p-4 group hover:border-rose-500/40 transition-all duration-300">
          <div className="absolute top-0 right-0 w-20 h-20 bg-rose-500/10 rounded-full blur-2xl group-hover:scale-150 transition-transform duration-500" />
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-rose-500/20">
              <TrendingDown className="h-5 w-5 text-rose-600" />
            </div>
            <div>
              <p className="text-xs text-muted-foreground font-medium">Total Expenses</p>
              <p className="text-xl font-bold text-rose-600">{formatINR(totalExpense)}</p>
            </div>
          </div>
        </div>
        <div className="relative overflow-hidden rounded-xl bg-gradient-to-br from-primary/10 via-primary/5 to-transparent border border-primary/20 p-4 group hover:border-primary/40 transition-all duration-300">
          <div className="absolute top-0 right-0 w-20 h-20 bg-primary/10 rounded-full blur-2xl group-hover:scale-150 transition-transform duration-500" />
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-primary/20">
              <Sparkles className="h-5 w-5 text-primary" />
            </div>
            <div>
              <p className="text-xs text-muted-foreground font-medium">Net Balance</p>
              <p className={cn("text-xl font-bold", totalIncome - totalExpense >= 0 ? "text-emerald-600" : "text-rose-600")}>
                {totalIncome - totalExpense >= 0 ? "+" : "-"}{formatINR(Math.abs(totalIncome - totalExpense))}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="relative flex-1 max-w-sm group">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground group-focus-within:text-primary transition-colors" />
          <Input
            placeholder="Search transactions..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 border-border/50 focus:border-primary/50 transition-all"
          />
        </div>
        <div className="flex items-center gap-2 flex-wrap">
          <Select value={selectedCategory} onValueChange={setSelectedCategory}>
            <SelectTrigger className="w-[180px] border-border/50">
              <Filter className="mr-2 h-4 w-4" />
              <SelectValue placeholder="All Categories" />
            </SelectTrigger>
            <SelectContent>
              {categories.map((category) => (
                <SelectItem key={category} value={category}>
                  <span className="flex items-center gap-2">
                    {category !== "All Categories" && <span>{categoryIcons[category]}</span>}
                    {category}
                  </span>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Main Content Tabs */}
      <Tabs defaultValue="table" className="w-full">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <TabsList className="bg-muted/50">
            <TabsTrigger value="table" className="gap-2 data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
              <Table2 className="h-4 w-4" />
              Table View
            </TabsTrigger>
            <TabsTrigger value="json" className="gap-2 data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
              <Code2 className="h-4 w-4" />
              Normalized JSON
            </TabsTrigger>
          </TabsList>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={() => handleDownload("raw")} className="gap-2 hover:bg-primary/10 hover:text-primary hover:border-primary/50 transition-all">
              <Download className="h-4 w-4" />
              Export Raw
            </Button>
            <Button size="sm" onClick={() => handleDownload("normalized")} className="gap-2 bg-primary hover:bg-primary/90">
              <Code2 className="h-4 w-4" />
              Export Normalized
            </Button>
          </div>
        </div>

        <TabsContent value="table" className="mt-4">
          <div className="rounded-xl border border-border/50 bg-card overflow-hidden shadow-sm">
            <Table>
              <TableHeader>
                <TableRow className="bg-muted/30 hover:bg-muted/30">
                  <TableHead 
                    className="cursor-pointer hover:bg-muted/50 transition-colors font-semibold"
                    onClick={() => handleSort("date")}
                  >
                    <div className="flex items-center gap-2">
                      Date
                      <ArrowUpDown className={cn("h-3 w-3 transition-colors", sortField === "date" && "text-primary")} />
                    </div>
                  </TableHead>
                  <TableHead className="font-semibold">Description</TableHead>
                  <TableHead className="font-semibold">Category</TableHead>
                  <TableHead className="font-semibold">Type</TableHead>
                  <TableHead 
                    className="text-right cursor-pointer hover:bg-muted/50 transition-colors font-semibold"
                    onClick={() => handleSort("amount")}
                  >
                    <div className="flex items-center justify-end gap-2">
                      Amount
                      <ArrowUpDown className={cn("h-3 w-3 transition-colors", sortField === "amount" && "text-primary")} />
                    </div>
                  </TableHead>
                  <TableHead className="w-12" />
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredTransactions.map((transaction, index) => (
                  <TableRow 
                    key={transaction.id} 
                    className={cn(
                      "transition-all duration-200 cursor-pointer",
                      hoveredRow === transaction.id ? "bg-primary/5 scale-[1.01]" : "hover:bg-muted/20",
                      selectedTransaction?.id === transaction.id && "bg-primary/10 border-l-2 border-l-primary"
                    )}
                    style={{ animationDelay: `${index * 30}ms` }}
                    onMouseEnter={() => setHoveredRow(transaction.id)}
                    onMouseLeave={() => setHoveredRow(null)}
                    onClick={() => setSelectedTransaction(selectedTransaction?.id === transaction.id ? null : transaction)}
                  >
                    <TableCell className="font-medium text-muted-foreground">
                      {transaction.date}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <span className="text-lg">{categoryIcons[transaction.category]}</span>
                        <span className="font-medium">{transaction.description}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge
                        variant="outline"
                        className={cn(
                          "text-xs font-medium border",
                          categoryColors[transaction.category]
                        )}
                      >
                        {transaction.category}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <Badge
                        className={cn(
                          "text-xs font-semibold border-0",
                          transaction.type === "Income" 
                            ? "bg-emerald-500/20 text-emerald-600 hover:bg-emerald-500/30" 
                            : "bg-rose-500/20 text-rose-600 hover:bg-rose-500/30"
                        )}
                      >
                        {transaction.type === "Income" ? "↗ Credit" : "↘ Debit"}
                      </Badge>
                    </TableCell>
                    <TableCell
                      className={cn(
                        "text-right font-bold tabular-nums",
                        transaction.amount >= 0 ? "text-emerald-600" : "text-rose-600"
                      )}
                    >
                      {transaction.amount >= 0 ? "+" : "-"}{formatINR(transaction.amount)}
                    </TableCell>
                    <TableCell>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8 opacity-0 group-hover:opacity-100 hover:bg-primary/10"
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedTransaction(transaction);
                        }}
                      >
                        <Eye className="h-4 w-4" />
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>

          {/* Selected Transaction Detail */}
          {selectedTransaction && (
            <div className="mt-4 rounded-xl border border-primary/20 bg-gradient-to-r from-primary/5 to-transparent p-4 animate-fade-in">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-semibold text-foreground flex items-center gap-2">
                  <Code2 className="h-4 w-4 text-primary" />
                  Transaction Details (Normalized)
                </h4>
                <Button variant="ghost" size="sm" onClick={() => setSelectedTransaction(null)} className="text-muted-foreground hover:text-foreground">
                  ✕
                </Button>
              </div>
              <pre className="text-xs bg-background/50 rounded-lg p-4 overflow-x-auto border border-border/50">
                <code className="text-foreground">{JSON.stringify(normalizeTransaction(selectedTransaction), null, 2)}</code>
              </pre>
            </div>
          )}
        </TabsContent>

        <TabsContent value="json" className="mt-4">
          <div className="rounded-xl border border-border/50 bg-card overflow-hidden shadow-sm">
            <div className="bg-muted/30 px-4 py-3 border-b border-border/50 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Code2 className="h-4 w-4 text-primary" />
                <span className="font-semibold text-sm">normalized_transactions.json</span>
                <Badge variant="secondary" className="text-xs">v1.0.0</Badge>
              </div>
              <span className="text-xs text-muted-foreground">{filteredTransactions.length} transactions</span>
            </div>
            <div className="max-h-[600px] overflow-auto">
              <pre className="text-sm p-4 leading-relaxed">
                <code className="text-foreground">{JSON.stringify(normalizedData, null, 2)}</code>
              </pre>
            </div>
          </div>
        </TabsContent>
      </Tabs>
      
      <p className="text-sm text-muted-foreground flex items-center gap-2">
        <Sparkles className="h-4 w-4 text-primary" />
        Showing {filteredTransactions.length} of {transactions.length} transactions
      </p>
    </div>
  );
};

export default TransactionTable;
