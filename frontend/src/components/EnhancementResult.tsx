"use client";

import React from "react";
import { Copy, Check, Info, Timer, Cpu, Hash } from "lucide-react";
import { Button } from "@/components/ui/button";

interface EnhancementResultProps {
  original: string;
  enhanced: string;
  metadata: any;
}

const MetadataTag = ({ icon: Icon, label, value }: { icon: any, label: string, value: string }) => (
  <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-zinc-800/50 border border-zinc-700/50 text-xs">
    <Icon size={14} className="text-blue-400" />
    <span className="text-zinc-500">{label}:</span>
    <span className="font-semibold text-zinc-200">{value}</span>
  </div>
);

export default function EnhancementResult({ original, enhanced, metadata }: EnhancementResultProps) {
  const [copied, setCopied] = React.useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(enhanced);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      {/* Metrics Row */}
      <div className="flex flex-wrap gap-3">
        <MetadataTag icon={Info} label="Framework" value={metadata.framework} />
        <MetadataTag icon={Cpu} label="Provider" value={metadata.target_provider} />
        <MetadataTag icon={Timer} label="Time" value={`${metadata.timing_ms?.toFixed(0) || "N/A"}ms`} />
        <MetadataTag icon={Hash} label="Tokens" value={`${metadata.estimated_tokens || "N/A"}`} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Before */}
        <div className="glass-card rounded-2xl p-6 border-zinc-800/50 flex flex-col h-full">
          <h3 className="text-sm font-semibold text-zinc-500 uppercase tracking-wider mb-4">Original</h3>
          <div className="flex-1 text-zinc-400 text-sm leading-relaxed whitespace-pre-wrap font-sans italic">
            {original}
          </div>
        </div>

        {/* After */}
        <div className="glass-card rounded-2xl p-6 border-blue-500/20 bg-blue-500/5 flex flex-col h-full shadow-lg shadow-blue-900/10">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-blue-400 uppercase tracking-wider">Enhanced Output</h3>
            <Button 
              size="sm" 
              variant="ghost" 
              onClick={handleCopy}
              className="h-8 gap-2 bg-blue-500/10 hover:bg-blue-500/20 text-blue-400"
            >
              {copied ? <Check size={14} /> : <Copy size={14} />}
              <span>{copied ? "Copied" : "Copy"}</span>
            </Button>
          </div>
          <div className="flex-1 text-zinc-100 text-base leading-relaxed whitespace-pre-wrap font-sans font-medium">
            {enhanced}
          </div>
        </div>
      </div>
    </div>
  );
}
