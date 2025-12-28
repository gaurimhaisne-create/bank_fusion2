import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { Transaction } from "@/context/TransactionContext";
import { useMemo } from "react";

interface IncomeExpenseChartProps {
  transactions?: Transaction[];
}

const formatINR = (value: number) => {
  if (value >= 1000) {
    return `₹${(value / 1000).toFixed(0)}k`;
  }
  return `₹${value}`;
};

const IncomeExpenseChart = ({ transactions }: IncomeExpenseChartProps) => {
  const monthlyData = useMemo(() => {
    if (!transactions || transactions.length === 0) {
      return [
        { month: "Aug", income: 38000, expenses: 28000 },
        { month: "Sep", income: 42000, expenses: 31000 },
        { month: "Oct", income: 45000, expenses: 33000 },
        { month: "Nov", income: 41000, expenses: 29000 },
        { month: "Dec", income: 48000, expenses: 35000 },
        { month: "Jan", income: 45625, expenses: 32168 },
      ];
    }

    const monthlyTotals: Record<string, { income: number; expenses: number }> = {};
    
    transactions.forEach(t => {
      const date = new Date(t.date);
      const monthKey = date.toLocaleString('en-US', { month: 'short' });
      
      if (!monthlyTotals[monthKey]) {
        monthlyTotals[monthKey] = { income: 0, expenses: 0 };
      }
      
      if (t.type === "Income") {
        monthlyTotals[monthKey].income += t.amount;
      } else {
        monthlyTotals[monthKey].expenses += Math.abs(t.amount);
      }
    });

    return Object.entries(monthlyTotals).map(([month, data]) => ({
      month,
      income: data.income,
      expenses: data.expenses,
    }));
  }, [transactions]);

  return (
    <div className="stat-card h-[360px] animate-fade-in">
      <h3 className="mb-4 text-lg font-semibold text-foreground">Income vs Expenses</h3>
      <ResponsiveContainer width="100%" height="85%">
        <AreaChart data={monthlyData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="incomeGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="hsl(142, 71%, 45%)" stopOpacity={0.3} />
              <stop offset="95%" stopColor="hsl(142, 71%, 45%)" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="expenseGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="hsl(0, 84%, 60%)" stopOpacity={0.3} />
              <stop offset="95%" stopColor="hsl(0, 84%, 60%)" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
          <XAxis
            dataKey="month"
            stroke="hsl(var(--muted-foreground))"
            fontSize={12}
            tickLine={false}
            axisLine={false}
          />
          <YAxis
            stroke="hsl(var(--muted-foreground))"
            fontSize={12}
            tickLine={false}
            axisLine={false}
            tickFormatter={(value) => formatINR(value)}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "hsl(var(--card))",
              border: "1px solid hsl(var(--border))",
              borderRadius: "8px",
              boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
            }}
            formatter={(value: number) => [`₹${value.toLocaleString('en-IN')}`, ""]}
          />
          <Legend 
            verticalAlign="bottom" 
            height={36}
            iconType="circle"
          />
          <Area
            type="monotone"
            dataKey="income"
            stroke="hsl(142, 71%, 45%)"
            strokeWidth={2}
            fill="url(#incomeGradient)"
            name="Income"
          />
          <Area
            type="monotone"
            dataKey="expenses"
            stroke="hsl(0, 84%, 60%)"
            strokeWidth={2}
            fill="url(#expenseGradient)"
            name="Expenses"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default IncomeExpenseChart;
