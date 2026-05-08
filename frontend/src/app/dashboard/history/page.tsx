"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import DashboardLayout from "@/components/DashboardLayout";
import { Loader2, History as HistoryIcon, ArrowRight, Calendar, Copy, Check } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function HistoryPage() {
  const [items, setItems] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [copiedId, setCopiedId] = useState<number | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await api.engine.history();
        setItems(data.items);
      } catch (err) {
        console.error("Failed to fetch history", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchHistory();
  }, []);

  const handleCopy = (text: string, id: number) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <DashboardLayout>
      <div className="mb-10">
        <h1 className="text-4xl font-bold text-white tracking-tight mb-2">Enhancement History</h1>
        <p className="text-zinc-500 text-lg">
          Review your previous optimizations and re-use enhanced prompts.
        </p>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-20">
          <Loader2 className="animate-spin text-blue-500" size={32} />
        </div>
      ) : items.length === 0 ? (
        <div className="glass-card rounded-2xl p-20 text-center border-dashed border-zinc-800">
          <div className="w-16 h-16 bg-zinc-900 rounded-full flex items-center justify-center mx-auto mb-6">
            <HistoryIcon className="text-zinc-600" size={32} />
          </div>
          <h2 className="text-xl font-bold text-zinc-300">No history found</h2>
          <p className="text-zinc-500 mt-2">Start enhancing prompts to see them here.</p>
        </div>
      ) : (
        <div className="space-y-6">
          {items.map((item) => (
            <div key={item.id} className="glass-card rounded-2xl p-6 border-zinc-800/50 hover:border-blue-500/30 transition-all group">
              <div className="flex items-start justify-between gap-4 mb-4">
                <div className="flex items-center gap-3">
                  <div className="px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 text-xs font-bold uppercase tracking-widest border border-blue-500/20">
                    {item.framework_used}
                  </div>
                  <div className="flex items-center gap-2 text-zinc-500 text-xs">
                    <Calendar size={14} />
                    {new Date(item.created_at).toLocaleDateString()}
                  </div>
                </div>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  onClick={() => handleCopy(item.enhanced_text, item.id)}
                  className="h-8 gap-2 bg-zinc-800/50 hover:bg-zinc-800 text-zinc-400"
                >
                  {copiedId === item.id ? <Check size={14} className="text-green-500" /> : <Copy size={14} />}
                  <span>{copiedId === item.id ? "Copied" : "Copy Result"}</span>
                </Button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <span className="text-[10px] font-bold text-zinc-600 uppercase tracking-tighter">Original</span>
                  <p className="text-sm text-zinc-500 line-clamp-2 italic">{item.original_text}</p>
                </div>
                <div className="space-y-2">
                  <span className="text-[10px] font-bold text-blue-900 uppercase tracking-tighter">Enhanced Result</span>
                  <p className="text-sm text-zinc-300 line-clamp-2">{item.enhanced_text}</p>
                </div>
              </div>
              
              <div className="mt-4 pt-4 border-t border-zinc-900 flex justify-end">
                <Button variant="link" className="text-blue-500 p-0 h-auto text-xs font-bold flex items-center gap-1 group-hover:gap-2 transition-all">
                  View Full Details <ArrowRight size={14} />
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}
    </DashboardLayout>
  );
}
