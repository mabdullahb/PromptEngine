"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import DashboardLayout from "@/components/DashboardLayout";
import UsageStats from "@/components/UsageStats";
import PromptEditor from "@/components/PromptEditor";
import EnhancementResult from "@/components/EnhancementResult";
import UsageProgress from "@/components/UsageProgress";
import UpgradePrompt from "@/components/UpgradePrompt";

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [usage, setUsage] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    const init = async () => {
      try {
        const [userData, usageData] = await Promise.all([
          api.auth.me(),
          api.get("/usage/summary")
        ]);
        setUser(userData);
        setUsage(usageData);
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
      // Refresh usage after success
      const usageData = await api.get("/usage/summary");
      setUsage(usageData);
    } catch (err) {
      console.error("Enhancement failed", err);
    } finally {
      setIsProcessing(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-zinc-950 text-white">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 rounded-full border-4 border-blue-500/20 border-t-blue-500 animate-spin" />
          <span className="text-zinc-500 font-medium">Initializing Engine...</span>
        </div>
      </div>
    );
  }

  return (
    <DashboardLayout>
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 mb-10">
        <div>
          <h1 className="text-4xl font-bold text-white tracking-tight mb-2">Prompt Editor</h1>
          <p className="text-zinc-500 text-lg">
            Craft, classify, and optimize your AI prompts.
          </p>
        </div>
        
        {usage && (
          <div className="w-full lg:w-72 glass-card rounded-2xl p-4">
            <UsageProgress 
              usage={usage.quota.usage} 
              limit={usage.quota.limit} 
              label={`${usage.plan} Quota`} 
            />
          </div>
        )}
      </div>

      <UsageStats />

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-12">
        <div className="xl:col-span-2 space-y-12">
          <section>
            <PromptEditor onEnhance={handleEnhance} isLoading={isProcessing} />
          </section>

          {result && (
            <section className="pt-8 border-t border-zinc-900 animate-in fade-in duration-700">
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

        <aside className="space-y-8">
          {usage?.plan === "free" && <UpgradePrompt />}
          
          <div className="glass-card rounded-2xl p-6 border-zinc-800/50">
            <h3 className="text-sm font-bold text-zinc-400 uppercase tracking-widest mb-4">Quick Insights</h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center text-sm">
                <span className="text-zinc-500">Last 30D Prompts</span>
                <span className="text-zinc-200 font-mono">{usage?.stats.total_prompts}</span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-zinc-500">Estimated ROI</span>
                <span className="text-green-400 font-bold">${usage?.stats.estimated_cost_usd} saved</span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </DashboardLayout>
  );
}
