"use client";

import React from "react";
import { TrendingUp, Zap, Clock, Box } from "lucide-react";

interface StatCardProps {
  label: string;
  value: string;
  subValue: string;
  icon: any;
  color: string;
}

const StatCard = ({ label, value, subValue, icon: Icon, color }: StatCardProps) => (
  <div className="glass-card rounded-2xl p-6 border-zinc-800/50 flex-1 min-w-[200px]">
    <div className="flex items-center gap-4 mb-4">
      <div className={`w-10 h-10 rounded-xl ${color} flex items-center justify-center`}>
        <Icon size={20} className="text-white" />
      </div>
      <span className="text-sm font-semibold text-zinc-500 uppercase tracking-wider">{label}</span>
    </div>
    <div className="flex flex-col">
      <span className="text-2xl font-bold text-zinc-100">{value}</span>
      <span className="text-xs text-zinc-500 mt-1">{subValue}</span>
    </div>
  </div>
);

export default function UsageStats() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <StatCard 
        label="Total Prompts" 
        value="128" 
        subValue="+12% from last week" 
        icon={Zap} 
        color="bg-amber-500 shadow-lg shadow-amber-500/20" 
      />
      <StatCard 
        label="Tokens Saved" 
        value="42.5k" 
        subValue="~32% efficiency boost" 
        icon={TrendingUp} 
        color="bg-green-500 shadow-lg shadow-green-500/20" 
      />
      <StatCard 
        label="Avg. Latency" 
        value="420ms" 
        subValue="-45ms improvement" 
        icon={Clock} 
        color="bg-blue-500 shadow-lg shadow-blue-500/20" 
      />
      <StatCard 
        label="Current Plan" 
        value="Pro Tier" 
        subValue="Unlimited enhancements" 
        icon={Box} 
        color="bg-purple-500 shadow-lg shadow-purple-500/20" 
      />
    </div>
  );
}
