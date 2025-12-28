import { useNavigate } from "react-router-dom";
import { CheckCircle, Upload, BarChart3, FileJson, ArrowRight, Shield, Zap, Eye } from "lucide-react";
import { Button } from "@/components/ui/button";
import Header from "@/components/Header";

const Index = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      {/* Hero Section */}
      <section className="container py-20 text-center">
        <div className="mx-auto max-w-3xl animate-fade-in">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full bg-primary/10 px-4 py-2 text-sm font-medium text-primary">
            <Zap className="h-4 w-4" />
            Intelligent Bank Statement Processing
          </div>
          <h1 className="mb-6 text-4xl font-bold tracking-tight text-foreground sm:text-5xl lg:text-6xl">
            Transform Your Bank Statements into{" "}
            <span className="text-primary">Actionable Insights</span>
          </h1>
          <p className="mb-8 text-lg text-muted-foreground">
            Upload your PDF bank statements and instantly extract, analyze, and visualize your financial data. 
            Export to JSON for seamless integration with your applications.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-4">
            <Button size="lg" onClick={() => navigate("/upload")} className="gap-2 shadow-lg shadow-primary/25">
              <Upload className="h-5 w-5" />
              Upload Statement
              <ArrowRight className="h-4 w-4" />
            </Button>
            <Button size="lg" variant="outline" onClick={() => navigate("/dashboard")}>
              View Demo Dashboard
            </Button>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="container py-16">
        <div className="mb-12 text-center">
          <h2 className="text-3xl font-bold text-foreground">Powerful Features</h2>
          <p className="mt-2 text-muted-foreground">Everything you need to manage your financial data</p>
        </div>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <div className="rounded-xl border border-border bg-card p-6 transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
              <Upload className="h-6 w-6 text-primary" />
            </div>
            <h3 className="mb-2 font-semibold text-foreground">PDF Upload</h3>
            <p className="text-sm text-muted-foreground">
              Drag and drop your bank statement PDFs for instant processing
            </p>
          </div>
          <div className="rounded-xl border border-border bg-card p-6 transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-income/10">
              <Eye className="h-6 w-6 text-income" />
            </div>
            <h3 className="mb-2 font-semibold text-foreground">Smart Extraction</h3>
            <p className="text-sm text-muted-foreground">
              AI-powered extraction identifies transactions and categories
            </p>
          </div>
          <div className="rounded-xl border border-border bg-card p-6 transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-chart-2/10">
              <BarChart3 className="h-6 w-6 text-chart-2" />
            </div>
            <h3 className="mb-2 font-semibold text-foreground">Visual Analytics</h3>
            <p className="text-sm text-muted-foreground">
              Interactive charts and insights for spending patterns
            </p>
          </div>
          <div className="rounded-xl border border-border bg-card p-6 transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-warning/10">
              <FileJson className="h-6 w-6 text-warning" />
            </div>
            <h3 className="mb-2 font-semibold text-foreground">JSON Export</h3>
            <p className="text-sm text-muted-foreground">
              Download structured data for integration or analysis
            </p>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="container py-16">
        <div className="mb-12 text-center">
          <h2 className="text-3xl font-bold text-foreground">How It Works</h2>
          <p className="mt-2 text-muted-foreground">Three simple steps to financial clarity</p>
        </div>
        <div className="grid gap-8 md:grid-cols-3">
          <div className="text-center">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-primary text-2xl font-bold text-primary-foreground">
              1
            </div>
            <h3 className="mb-2 text-lg font-semibold text-foreground">Upload PDF</h3>
            <p className="text-muted-foreground">
              Simply drag and drop your bank statement PDF files
            </p>
          </div>
          <div className="text-center">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-primary text-2xl font-bold text-primary-foreground">
              2
            </div>
            <h3 className="mb-2 text-lg font-semibold text-foreground">Process & Extract</h3>
            <p className="text-muted-foreground">
              Our system automatically extracts and categorizes transactions
            </p>
          </div>
          <div className="text-center">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-primary text-2xl font-bold text-primary-foreground">
              3
            </div>
            <h3 className="mb-2 text-lg font-semibold text-foreground">Analyze & Export</h3>
            <p className="text-muted-foreground">
              View insights on dashboard or download JSON data
            </p>
          </div>
        </div>
      </section>

      {/* Trust Section */}
      <section className="container py-16">
        <div className="rounded-2xl bg-card border border-border p-8 md:p-12">
          <div className="flex flex-col items-center text-center md:flex-row md:text-left">
            <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-primary/10 md:mb-0 md:mr-6">
              <Shield className="h-8 w-8 text-primary" />
            </div>
            <div className="flex-1">
              <h3 className="mb-2 text-xl font-semibold text-foreground">Your Data is Secure</h3>
              <p className="text-muted-foreground">
                All file processing happens locally in your browser. Your sensitive financial data never leaves your device, 
                ensuring complete privacy and security.
              </p>
            </div>
            <Button 
              size="lg" 
              onClick={() => navigate("/upload")} 
              className="mt-6 md:mt-0 md:ml-6"
            >
              Get Started
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border bg-card/50 py-8">
        <div className="container flex flex-col items-center justify-between gap-4 md:flex-row">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
              <CheckCircle className="h-4 w-4 text-primary-foreground" />
            </div>
            <span className="font-semibold text-foreground">FinSight</span>
          </div>
          <p className="text-sm text-muted-foreground">
            © 2024 FinSight. Secure bank statement processing.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
