import { ArrowUpRight, ArrowDownRight } from "lucide-react";
import { cn } from "@/lib/utils";
import { Transaction } from "@/context/TransactionContext";

interface RecentTransactionsProps {
  transactions?: Transaction[];
}

const formatINR = (amount: number) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 2,
  }).format(Math.abs(amount));
};

const defaultTransactions: Transaction[] = [
  { id: "1", date: "2024-01-15", description: "Salary Deposit", category: "Income", amount: 35000.00, type: "Income" },
  { id: "2", date: "2024-01-16", description: "Rent Payment", category: "Housing", amount: -12000.00, type: "Expense" },
  { id: "3", date: "2024-01-17", description: "Grocery Shopping", category: "Groceries", amount: -2850.00, type: "Expense" },
  { id: "4", date: "2024-01-18", description: "Freelance Project", category: "Income", amount: 8500.00, type: "Expense" },
  { id: "5", date: "2024-01-19", description: "Electric Bill", category: "Utilities", amount: -1850.00, type: "Expense" },
];

const RecentTransactions = ({ transactions }: RecentTransactionsProps) => {
  const displayTransactions = transactions && transactions.length > 0 ? transactions : defaultTransactions;

  return (
    <div className="stat-card animate-fade-in">
      <h3 className="mb-4 text-lg font-semibold text-foreground">Recent Transactions</h3>
      <div className="space-y-3">
        {displayTransactions.map((transaction) => (
          <div
            key={transaction.id}
            className="flex items-center justify-between rounded-lg border border-border/50 p-3 transition-all duration-200 hover:bg-muted/50"
          >
            <div className="flex items-center gap-3">
              <div
                className={cn(
                  "flex h-9 w-9 items-center justify-center rounded-full",
                  transaction.type === "Income" ? "bg-income/10" : "bg-expense/10"
                )}
              >
                {transaction.type === "Income" ? (
                  <ArrowUpRight className="h-4 w-4 text-income" />
                ) : (
                  <ArrowDownRight className="h-4 w-4 text-expense" />
                )}
              </div>
              <div>
                <p className="font-medium text-foreground">{transaction.description}</p>
                <p className="text-xs text-muted-foreground">{transaction.category} • {transaction.date}</p>
              </div>
            </div>
            <p
              className={cn(
                "font-semibold",
                transaction.type === "Income" ? "amount-positive" : "amount-negative"
              )}
            >
              {transaction.type === "Income" ? "+" : "-"}{formatINR(transaction.amount)}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecentTransactions;
