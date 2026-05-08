"use client";

import React from "react";
import Link from "next/link";
import { Check, Sparkles, Zap, Users } from "lucide-react";
import { Button } from "@/components/ui/button";

const FeatureItem = ({ text }: { text: string }) => (
  <li className="flex items-start gap-3 text-sm text-zinc-400">
    <div className="mt-0.5 text-blue-500"><Check size={16} /></div>
    {text}
  </li>
);

export default function PricingPage() {
  return (
    <div className="min-h-screen bg-zinc-950 text-white bg-grid py-20 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-black tracking-tight mb-4">Pricing that scales with you</h1>
          <p className="text-zinc-500 text-xl max-w-2xl mx-auto">
            Choose the perfect plan for your prompt engineering needs. From solo hackers to enterprise teams.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Free */}
          <div className="glass-card rounded-3xl p-8 border-zinc-800/50 flex flex-col h-full hover:border-zinc-700 transition-all">
            <div className="mb-8">
              <div className="w-12 h-12 bg-zinc-900 rounded-2xl flex items-center justify-center mb-4">
                <Zap size={24} className="text-zinc-500" />
              </div>
              <h2 className="text-2xl font-bold uppercase tracking-tighter">Free</h2>
              <div className="flex items-baseline gap-1 mt-2">
                <span className="text-4xl font-black">$0</span>
                <span className="text-zinc-500 text-sm">/forever</span>
              </div>
            </div>
            <ul className="space-y-4 mb-10 flex-1">
              <FeatureItem text="10 enhancements per day" />
              <FeatureItem text="Community support" />
              <FeatureItem text="Basic frameworks (RTF, Role)" />
              <FeatureItem text="Standard AI models" />
            </ul>
            <Link href="/register">
              <Button variant="outline" className="w-full py-6 rounded-2xl border-zinc-700 text-zinc-300">Get Started</Button>
            </Link>
          </div>

          {/* Pro */}
          <div className="glass-card rounded-3xl p-8 border-blue-500/30 bg-blue-500/5 flex flex-col h-full relative transform scale-105 shadow-2xl shadow-blue-500/10">
            <div className="absolute top-0 right-8 transform -translate-y-1/2">
              <div className="bg-blue-600 text-white text-[10px] font-black px-4 py-1.5 rounded-full uppercase tracking-widest shadow-xl">Most Popular</div>
            </div>
            <div className="mb-8">
              <div className="w-12 h-12 bg-blue-600 rounded-2xl flex items-center justify-center mb-4 shadow-lg shadow-blue-600/30">
                <Sparkles size={24} className="text-white" />
              </div>
              <h2 className="text-2xl font-bold uppercase tracking-tighter">Pro</h2>
              <div className="flex items-baseline gap-1 mt-2">
                <span className="text-4xl font-black">$19.99</span>
                <span className="text-zinc-500 text-sm">/month</span>
              </div>
            </div>
            <ul className="space-y-4 mb-10 flex-1">
              <FeatureItem text="1,000 enhancements per day" />
              <FeatureItem text="Advanced frameworks (CoT, CRISPE)" />
              <FeatureItem text="Priority model access" />
              <FeatureItem text="Stripe billing dashboard" />
              <FeatureItem text="Priority email support" />
            </ul>
            <Link href="/register?plan=pro">
              <Button className="w-full py-6 rounded-2xl bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-600/20 font-bold">Try Pro Now</Button>
            </Link>
          </div>

          {/* Team */}
          <div className="glass-card rounded-3xl p-8 border-zinc-800/50 flex flex-col h-full hover:border-zinc-700 transition-all">
            <div className="mb-8">
              <div className="w-12 h-12 bg-zinc-900 rounded-2xl flex items-center justify-center mb-4">
                <Users size={24} className="text-zinc-500" />
              </div>
              <h2 className="text-2xl font-bold uppercase tracking-tighter">Team</h2>
              <div className="flex items-baseline gap-1 mt-2">
                <span className="text-4xl font-black">$49.99</span>
                <span className="text-zinc-500 text-sm">/month</span>
              </div>
            </div>
            <ul className="space-y-4 mb-10 flex-1">
              <FeatureItem text="Unlimited enhancements" />
              <FeatureItem text="Shared team workspaces" />
              <FeatureItem text="Custom framework builder" />
              <FeatureItem text="Dedicated account manager" />
              <FeatureItem text="SLA-backed uptime" />
            </ul>
            <Link href="/register?plan=team">
              <Button variant="outline" className="w-full py-6 rounded-2xl border-zinc-700 text-zinc-300">Contact Sales</Button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
