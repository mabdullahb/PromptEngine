"use client";

import React, { Component, ErrorInfo, ReactNode } from "react";
import { AlertTriangle, RefreshCcw } from "lucide-react";
import { Button } from "@/components/ui/button";

interface Props {
  children?: ReactNode;
}

interface State {
  hasError: boolean;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(_: Error): State {
    return { hasError: true };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error:", error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-zinc-950 p-6">
          <div className="glass-card rounded-3xl p-10 max-w-md text-center border-red-500/20">
            <div className="w-16 h-16 bg-red-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
              <AlertTriangle className="text-red-500" size={32} />
            </div>
            <h1 className="text-2xl font-bold text-white mb-2">Something went wrong</h1>
            <p className="text-zinc-500 mb-8">
              An unexpected error occurred in the dashboard. Please try refreshing the page.
            </p>
            <Button 
              onClick={() => window.location.reload()}
              className="bg-zinc-800 hover:bg-zinc-700 text-white gap-2 px-8 py-6 rounded-xl font-bold"
            >
              <RefreshCcw size={18} />
              Refresh Dashboard
            </Button>
          </div>
        </div>
      );
    }

    return this.children;
  }
}

export default ErrorBoundary;
