"use client";

import React from "react";

interface UsageProgressProps {
  usage: number;
  limit: number;
  label: string;
}

export default function UsageProgress({ usage, limit, label }: UsageProgressProps) {
  const percentage = Math.min((usage / limit) * 100, 100);
  const isNearLimit = percentage > 80;
  const isAtLimit = percentage >= 100;

  return (
    <div className="space-y-2">
      <div className="flex justify-between items-center text-xs font-semibold uppercase tracking-wider">
        <span className="text-zinc-500">{label}</span>
        <span className={isAtLimit ? "text-red-400" : isNearLimit ? "text-amber-400" : "text-zinc-300"}>
          {usage} / {limit}
        </span>
      </div>
      <div className="h-2 w-full bg-zinc-900 rounded-full overflow-hidden border border-zinc-800">
        <div 
          className={`h-full transition-all duration-500 rounded-full ${
            isAtLimit ? "bg-red-500" : isNearLimit ? "bg-amber-500" : "bg-blue-600"
          }`}
          style={{ width: `${percentage}%` }}
        />
      </div>
      {isAtLimit && (
        <p className="text-[10px] text-red-400 font-medium">Daily limit reached. Upgrade to keep enhancing!</p>
      )}
    </div>
  );
}
