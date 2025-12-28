import { Wallet, TrendingUp, TrendingDown, PiggyBank, Upload } from "lucide-react";
import { useNavigate } from "react-router-dom";
import Header from "@/components/Header";
import StatCard from "@/components/StatCard";
import ExpenseChart from "@/components/ExpenseChart";
import IncomeExpenseChart from "@/components/IncomeExpenseChart";
import RecentTransactions from "@/components/RecentTransactions";
import { Button } from "@/components/ui/button";
import { useTransactions } from "@/context/TransactionContext";

const formatINR = (amount: number) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 2,
  }).format(amount);
};

const Dashboard = () => {
  const navigate = useNavigate();
  const { statements, getTotalIncome, getTotalExpenses, getTotalBalance, getSavingsRate, getAllTransactions } = useTransactions();

  const hasData = statements.length > 0;
  const totalIncome = getTotalIncome();
  const totalExpenses = getTotalExpenses();
  const totalBalance = getTotalBalance();
  const savingsRate = getSavingsRate();
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
            <h1 className="text-2xl font-bold text-foreground mb-2">No Data Available</h1>
            <p className="text-muted-foreground mb-6 max-w-md">
              Upload a bank statement PDF to see your financial overview, spending patterns, and transaction history.
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

  // Calculate change percentages (mock for now)
  const incomeChange = "↑ 8.2% from last month";
  const expenseChange = totalExpenses < totalIncome ? "↓ 3.1% from last month" : "↑ 5.2% from last month";
  const savingsChange = savingsRate > 20 ? "↑ 5.4% from last month" : "↓ 2.1% from last month";

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container py-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-foreground">Financial Overview</h1>
          <p className="text-muted-foreground">
            Data from {statements.length} statement(s) • {transactions.length} transactions
          </p>
        </div>

        {/* Stats Grid */}
        <div className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard
            title="Total Balance"
            value={formatINR(totalBalance)}
            change={totalBalance >= 0 ? "↑ 12.5% from last month" : "↓ 5.2% from last month"}
            changeType={totalBalance >= 0 ? "positive" : "negative"}
            icon={Wallet}
            iconColor="bg-primary/10 text-primary"
          />
          <StatCard
            title="Total Income"
            value={formatINR(totalIncome)}
            change={incomeChange}
            changeType="positive"
            icon={TrendingUp}
            iconColor="bg-income/10 text-income"
          />
          <StatCard
            title="Total Expenses"
            value={formatINR(totalExpenses)}
            change={expenseChange}
            changeType="negative"
            icon={TrendingDown}
            iconColor="bg-expense/10 text-expense"
          />
          <StatCard
            title="Savings Rate"
            value={`${savingsRate.toFixed(1)}%`}
            change={savingsChange}
            changeType={savingsRate > 20 ? "positive" : "negative"}
            icon={PiggyBank}
            iconColor="bg-chart-2/10 text-chart-2"
          />
        </div>

        {/* Charts Row */}
        <div className="mb-8 grid gap-6 lg:grid-cols-2">
          <ExpenseChart transactions={transactions} />
          <IncomeExpenseChart transactions={transactions} />
        </div>

        {/* Recent Transactions */}
        <RecentTransactions transactions={transactions.slice(0, 5)} />
      </main>
    </div>
  );
};

export default Dashboard;
