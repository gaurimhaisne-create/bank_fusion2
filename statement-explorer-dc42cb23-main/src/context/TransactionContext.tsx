import { createContext, useContext, useState, ReactNode } from "react";

export interface Transaction {
  id: string;
  date: string;
  description: string;
  category: string;
  amount: number;
  type: "Income" | "Expense";
}

export interface BankStatement {
  fileName: string;
  accountHolder: string;
  accountNumber: string;
  statementPeriod: string;
  openingBalance: number;
  closingBalance: number;
  totalCredits: number;
  totalDebits: number;
  transactions: Transaction[];
  uploadedAt: string;
}

interface TransactionContextType {
  statements: BankStatement[];
  addStatement: (statement: BankStatement) => void;
  clearStatements: () => void;
  getAllTransactions: () => Transaction[];
  getTotalIncome: () => number;
  getTotalExpenses: () => number;
  getTotalBalance: () => number;
  getSavingsRate: () => number;
}

const TransactionContext = createContext<TransactionContextType | undefined>(undefined);

export const TransactionProvider = ({ children }: { children: ReactNode }) => {
  const [statements, setStatements] = useState<BankStatement[]>([]);

  const addStatement = (statement: BankStatement) => {
    setStatements((prev) => [...prev, statement]);
  };

  const clearStatements = () => {
    setStatements([]);
  };

  const getAllTransactions = (): Transaction[] => {
    return statements.flatMap((s) => s.transactions);
  };

  const getTotalIncome = (): number => {
    return getAllTransactions()
      .filter((t) => t.type === "Income")
      .reduce((sum, t) => sum + t.amount, 0);
  };

  const getTotalExpenses = (): number => {
    return getAllTransactions()
      .filter((t) => t.type === "Expense")
      .reduce((sum, t) => sum + Math.abs(t.amount), 0);
  };

  const getTotalBalance = (): number => {
    return getTotalIncome() - getTotalExpenses();
  };

  const getSavingsRate = (): number => {
    const income = getTotalIncome();
    if (income === 0) return 0;
    return ((income - getTotalExpenses()) / income) * 100;
  };

  return (
    <TransactionContext.Provider
      value={{
        statements,
        addStatement,
        clearStatements,
        getAllTransactions,
        getTotalIncome,
        getTotalExpenses,
        getTotalBalance,
        getSavingsRate,
      }}
    >
      {children}
    </TransactionContext.Provider>
  );
};

export const useTransactions = () => {
  const context = useContext(TransactionContext);
  if (!context) {
    throw new Error("useTransactions must be used within a TransactionProvider");
  }
  return context;
};
