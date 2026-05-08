"use client";

import React from "react";
import Link from "next/link";
import { Sparkles, ArrowRight } from "lucide-react";

export default function UpgradePrompt() {
  return (
    <div className="glass-card rounded-2xl p-6 border-blue-500/30 bg-blue-500/5 relative overflow-hidden group">
      <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:opacity-20 transition-opacity">
        <Sparkles size={120} className="text-blue-400" />
      </div>
      
      <div className="relative z-10">
        <h3 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
          Unlock Pro Power <Sparkles size={20} className="text-blue-400" />
        </h3>
        <p className="text-zinc-400 text-sm mb-6 max-w-md">
          You're using the Free tier. Upgrade to Pro for 1,000 enhancements per day, 
          priority model access, and advanced engineering frameworks.
        </p>
        
        <Link 
          href="/dashboard/settings" 
          className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-6 py-2.5 rounded-xl font-bold text-sm transition-all shadow-lg shadow-blue-600/20 active:scale-95"
        >
          View Plans <ArrowRight size={16} />
        </Link>
      </div>
    </div>
  );
}
