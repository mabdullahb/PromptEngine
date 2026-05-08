"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import DashboardLayout from "@/components/DashboardLayout";
import { Loader2, CreditCard, Check, Zap, Users, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function SettingsPage() {
  const [plans, setPlans] = useState<any[]>([]);
  const [currentUsage, setCurrentUsage] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isRedirecting, setIsRedirecting] = useState<string | null>(null);

  useEffect(() => {
    const init = async () => {
      try {
        const [plansData, usageData] = await Promise.all([
          api.get("/billing/plans"),
          api.get("/usage/summary")
        ]);
        setPlans(plansData);
        setCurrentUsage(usageData);
      } catch (err) {
        console.error("Failed to load settings", err);
      } finally {
        setIsLoading(false);
      }
    };
    init();
  }, []);

  const handleUpgrade = async (planId: string) => {
    setIsRedirecting(planId);
    try {
      const data = await api.post(`/billing/checkout/${planId}`, {});
      window.location.href = data.checkout_url;
    } catch (err) {
      console.error("Checkout failed", err);
      setIsRedirecting(null);
    }
  };

  const handlePortal = async () => {
    try {
      const data = await api.get("/billing/portal");
      window.location.href = data.portal_url;
    } catch (err) {
      console.error("Portal redirect failed", err);
    }
  };

  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="flex justify-center py-20">
          <Loader2 className="animate-spin text-blue-500" size={32} />
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="mb-10">
        <h1 className="text-4xl font-bold text-white tracking-tight mb-2">Subscription & Billing</h1>
        <p className="text-zinc-500 text-lg">Manage your plan, billing details, and usage limits.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
        {plans.map((plan) => (
          <div 
            key={plan.id} 
            className={`glass-card rounded-3xl p-8 border-zinc-800/50 flex flex-col relative overflow-hidden ${
              currentUsage?.plan === plan.id ? "ring-2 ring-blue-500/50 border-blue-500/20" : ""
            }`}
          >
            {currentUsage?.plan === plan.id && (
              <div className="absolute top-4 right-4 px-3 py-1 bg-blue-500/10 text-blue-400 text-[10px] font-bold rounded-full border border-blue-500/20">
                CURRENT PLAN
              </div>
            )}
            
            <div className="mb-8">
              <h3 className="text-xl font-bold text-white mb-2 uppercase tracking-tight">{plan.name}</h3>
              <div className="flex items-baseline gap-1">
                <span className="text-4xl font-black text-white">${plan.price}</span>
                <span className="text-zinc-500 text-sm">/month</span>
              </div>
            </div>

            <ul className="space-y-4 mb-10 flex-1">
              {plan.features.map((feature: string) => (
                <li key={feature} className="flex items-start gap-3 text-sm text-zinc-400">
                  <div className="mt-0.5 text-blue-500"><Check size={16} /></div>
                  {feature}
                </li>
              ))}
            </ul>

            <Button
              disabled={currentUsage?.plan === plan.id || isRedirecting !== null}
              onClick={() => handleUpgrade(plan.id)}
              className={`w-full py-6 rounded-2xl font-bold text-sm transition-all ${
                currentUsage?.plan === plan.id 
                  ? "bg-zinc-800 text-zinc-500 cursor-not-allowed" 
                  : "bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-600/20"
              }`}
            >
              {isRedirecting === plan.id ? (
                <Loader2 className="animate-spin" size={18} />
              ) : currentUsage?.plan === plan.id ? (
                "Active Plan"
              ) : (
                `Get ${plan.name}`
              )}
            </Button>
          </div>
        ))}
      </div>

      <div className="glass-card rounded-2xl p-8 border-zinc-800/50">
        <div className="flex items-center justify-between gap-6 flex-wrap">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-zinc-800 flex items-center justify-center text-zinc-400">
              <CreditCard size={24} />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">Payment Method</h3>
              <p className="text-zinc-500 text-sm">Manage your saved cards and billing history in Stripe.</p>
            </div>
          </div>
          <Button 
            variant="outline" 
            onClick={handlePortal}
            className="rounded-xl px-6 border-zinc-700 text-zinc-300 hover:bg-zinc-800"
          >
            Manage Billing <ArrowRight size={16} className="ml-2" />
          </Button>
        </div>
      </div>
    </DashboardLayout>
  );
}
