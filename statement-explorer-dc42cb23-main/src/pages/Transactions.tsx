import { useNavigate } from "react-router-dom";
import { Upload } from "lucide-react";
import Header from "@/components/Header";
import TransactionTable from "@/components/TransactionTable";
import { Button } from "@/components/ui/button";
import { useTransactions } from "@/context/TransactionContext";

const Transactions = () => {
  const navigate = useNavigate();
  const { statements, getAllTransactions } = useTransactions();

  const hasData = statements.length > 0;
  const transactions = getAllTransactions();

  if (!hasData) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <main className="container py-8">
          <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
            <div className="flex h-20 w-20 items-center justify-center rounded-full bg-primary/10 mb-6">
              <Upload className="h-10 w-10 text-primary" />
            </div>
            <h1 className="text-2xl font-bold text-foreground mb-2">No Transactions</h1>
            <p className="text-muted-foreground mb-6 max-w-md">
              Upload a bank statement PDF to view and analyze all your transactions.
            </p>
            <Button onClick={() => navigate("/upload")} size="lg" className="gap-2">
              <Upload className="h-5 w-5" />
              Upload Bank Statement
            </Button>
          </div>
        </main>
      </div>
    );
  }

  // Convert transactions to the format expected by TransactionTable
  const formattedTransactions = transactions.map((t) => ({
    id: t.id,
    date: t.date,
    description: t.description,
    category: t.category,
    amount: t.amount,
    type: t.type,
  }));

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container py-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-foreground">Transactions</h1>
          <p className="text-muted-foreground">
            {transactions.length} transactions from {statements.length} statement(s)
          </p>
        </div>

        <div className="rounded-xl bg-card p-6 shadow-sm border border-border/30">
          <TransactionTable transactions={formattedTransactions} />
        </div>
      </main>
    </div>
  );
};

export default Transactions;
