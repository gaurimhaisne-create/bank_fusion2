import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts";
import { Transaction } from "@/context/TransactionContext";
import { useMemo } from "react";

interface ExpenseChartProps {
  transactions?: Transaction[];
}

const categoryColors: Record<string, string> = {
  Housing: "hsl(221, 83%, 53%)",
  Groceries: "hsl(142, 71%, 45%)",
  Utilities: "hsl(38, 92%, 50%)",
  Shopping: "hsl(280, 65%, 60%)",
  Food: "hsl(0, 84%, 60%)",
  Healthcare: "hsl(199, 89%, 48%)",
  Transport: "hsl(24, 95%, 53%)",
  Entertainment: "hsl(160, 60%, 45%)",
  Income: "hsl(142, 71%, 45%)",
};

const formatINR = (amount: number) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 0,
  }).format(amount);
};

const ExpenseChart = ({ transactions }: ExpenseChartProps) => {
  const expenseData = useMemo(() => {
    if (!transactions || transactions.length === 0) {
      return [
        { name: "Housing", value: 67, amount: 12000, color: categoryColors.Housing },
        { name: "Groceries", value: 16, amount: 2850, color: categoryColors.Groceries },
        { name: "Utilities", value: 10, amount: 1850, color: categoryColors.Utilities },
        { name: "Others", value: 7, amount: 1200, color: categoryColors.Shopping },
      ];
    }

    const expenses = transactions.filter(t => t.type === "Expense");
    const totalExpense = expenses.reduce((sum, t) => sum + Math.abs(t.amount), 0);

    const categoryTotals: Record<string, number> = {};
    expenses.forEach(t => {
      categoryTotals[t.category] = (categoryTotals[t.category] || 0) + Math.abs(t.amount);
    });

    return Object.entries(categoryTotals)
      .map(([name, amount]) => ({
        name,
        value: Math.round((amount / totalExpense) * 100),
        amount,
        color: categoryColors[name] || "hsl(200, 50%, 50%)",
      }))
      .sort((a, b) => b.value - a.value);
  }, [transactions]);

  return (
    <div className="stat-card h-[360px] animate-fade-in">
      <h3 className="mb-4 text-lg font-semibold text-foreground">Expense Breakdown</h3>
      <ResponsiveContainer width="100%" height="85%">
        <PieChart>
          <Pie
            data={expenseData}
            cx="50%"
            cy="45%"
            innerRadius={60}
            outerRadius={100}
            paddingAngle={2}
            dataKey="value"
            label={({ name, value }) => `${name} ${value}%`}
            labelLine={{ stroke: "hsl(var(--muted-foreground))", strokeWidth: 1 }}
          >
            {expenseData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: "hsl(var(--card))",
              border: "1px solid hsl(var(--border))",
              borderRadius: "8px",
              boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
            }}
            formatter={(value: number, name: string, props: any) => [
              `${formatINR(props.payload.amount)} (${value}%)`,
              props.payload.name
            ]}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ExpenseChart;
