"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import DashboardLayout from "@/components/DashboardLayout";
import UsageStats from "@/components/UsageStats";
import PromptEditor from "@/components/PromptEditor";
import EnhancementResult from "@/components/EnhancementResult";
import { Loader2 } from "lucide-react";

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    const init = async () => {
      try {
        const userData = await api.auth.me();
        setUser(userData);
      } catch (err) {
        console.error("Auth initialization failed", err);
        router.push("/login");
      } finally {
        setIsLoading(false);
      }
    };

    init();
  }, [router]);

  const handleEnhance = async (prompt: string) => {
    setIsProcessing(true);
    try {
      const data = await api.engine.enhance(prompt);
      setResult(data);
    } catch (err) {
      console.error("Enhancement failed", err);
      // In a real app, show a toast here
    } finally {
      setIsProcessing(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-zinc-950 text-white">
        <Loader2 className="animate-spin text-blue-500" size={32} />
      </div>
    );
  }

  return (
    <DashboardLayout>
      <div className="mb-10">
        <h1 className="text-4xl font-bold text-white tracking-tight mb-2">Prompt Editor</h1>
        <p className="text-zinc-500 text-lg">
          Craft, classify, and optimize your AI prompts using our advanced enhancement engine.
        </p>
      </div>

      <UsageStats />

      <div className="space-y-12">
        <section>
          <PromptEditor onEnhance={handleEnhance} isLoading={isProcessing} />
        </section>

        {result && (
          <section className="pt-8 border-t border-zinc-900">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-2 h-8 bg-blue-500 rounded-full" />
              <h2 className="text-2xl font-bold text-white">Enhancement Results</h2>
            </div>
            <EnhancementResult 
              original={result.original_prompt} 
              enhanced={result.enhanced_prompt} 
              metadata={result.metadata} 
            />
          </section>
        )}
      </div>
    </DashboardLayout>
  );
}
