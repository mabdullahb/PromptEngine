"use client";

import React, { useState } from "react";
import { Sparkles, ArrowRight, Zap, Target, ShieldCheck, X } from "lucide-react";
import { Button } from "@/components/ui/button";

interface OnboardingModalProps {
  onComplete: () => void;
}

const steps = [
  {
    title: "Welcome to PromptEngine",
    description: "The ultimate platform for professional prompt engineering. Let's get you set up in 30 seconds.",
    icon: Sparkles,
    color: "text-blue-500 bg-blue-500/10"
  },
  {
    title: "Input & Classify",
    description: "Enter your raw prompt, and our engine automatically identifies its intent and optimal AI provider.",
    icon: Target,
    color: "text-amber-500 bg-amber-500/10"
  },
  {
    title: "Framework Enhancement",
    description: "We use advanced frameworks like COSTAR and CRISPE to rewrite your prompt for maximum AI performance.",
    icon: Zap,
    color: "text-purple-500 bg-purple-500/10"
  },
  {
    title: "Ready to Launch",
    description: "You're all set! Start optimizing your prompts and check your daily usage on the dashboard.",
    icon: ShieldCheck,
    color: "text-green-500 bg-green-500/10"
  }
];

export default function OnboardingModal({ onComplete }: OnboardingModalProps) {
  const [currentStep, setCurrentStep] = useState(0);

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      onComplete();
    }
  };

  const StepIcon = steps[currentStep].icon;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 backdrop-blur-sm animate-in fade-in duration-300">
      <div className="glass-card w-full max-w-lg rounded-3xl p-10 border-zinc-800/50 shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-1 bg-zinc-800">
          <div 
            className="h-full bg-blue-600 transition-all duration-500" 
            style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
          />
        </div>

        <button 
          onClick={onComplete}
          className="absolute top-6 right-6 text-zinc-500 hover:text-white transition-colors"
        >
          <X size={20} />
        </button>

        <div className="flex flex-col items-center text-center">
          <div className={`w-16 h-16 rounded-2xl flex items-center justify-center mb-8 ${steps[currentStep].color}`}>
            <StepIcon size={32} />
          </div>

          <h2 className="text-3xl font-bold text-white mb-4 tracking-tight">
            {steps[currentStep].title}
          </h2>
          
          <p className="text-zinc-400 text-lg leading-relaxed mb-10 max-w-sm">
            {steps[currentStep].description}
          </p>

          <Button 
            onClick={handleNext}
            className="w-full py-6 rounded-2xl bg-blue-600 hover:bg-blue-500 text-white font-bold flex items-center justify-center gap-2 shadow-lg shadow-blue-600/20"
          >
            {currentStep === steps.length - 1 ? "Start Engineering" : "Next Step"}
            <ArrowRight size={18} />
          </Button>

          <div className="flex gap-2 mt-8">
            {steps.map((_, idx) => (
              <div 
                key={idx}
                className={`w-1.5 h-1.5 rounded-full transition-all duration-300 ${
                  idx === currentStep ? "w-6 bg-blue-600" : "bg-zinc-800"
                }`}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
