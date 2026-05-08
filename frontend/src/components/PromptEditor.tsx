"use client";

import React, { useState } from "react";
import { Sparkles, Loader2, Send } from "lucide-react";
import { Button } from "@/components/ui/button";

interface PromptEditorProps {
  onEnhance: (prompt: string) => void;
  isLoading: boolean;
}

export default function PromptEditor({ onEnhance, isLoading }: PromptEditorProps) {
  const [prompt, setPrompt] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim() && !isLoading) {
      onEnhance(prompt);
    }
  };

  return (
    <div className="glass-card rounded-2xl p-6 shadow-2xl border border-zinc-800/50">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex items-center justify-between mb-2">
          <label className="text-sm font-semibold text-zinc-400 uppercase tracking-wider">
            Original Prompt
          </label>
          <div className="text-xs text-zinc-500 font-mono">
            {prompt.length} characters | ~{Math.ceil(prompt.length / 4)} tokens
          </div>
        </div>
        
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your raw prompt here... (e.g., 'Write a python script to parse logs')"
          className="w-full h-48 bg-zinc-950/50 border border-zinc-800 rounded-xl p-4 text-zinc-100 placeholder:text-zinc-600 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all resize-none font-sans text-lg leading-relaxed shadow-inner"
        />

        <div className="flex justify-end pt-2">
          <Button 
            type="submit"
            disabled={!prompt.trim() || isLoading}
            className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-6 rounded-xl font-bold flex items-center gap-2 shadow-lg shadow-blue-600/20 active:scale-95 transition-all h-auto"
          >
            {isLoading ? (
              <>
                <Loader2 size={20} className="animate-spin" />
                <span>Processing...</span>
              </>
            ) : (
              <>
                <Sparkles size={20} />
                <span>Enhance Prompt</span>
              </>
            )}
          </Button>
        </div>
      </form>
    </div>
  );
}
