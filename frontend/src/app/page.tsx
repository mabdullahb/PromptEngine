import Link from "next/link";
import { Sparkles, ArrowRight, ShieldCheck, Zap, Layers } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div className="min-h-screen bg-zinc-950 text-white overflow-hidden relative">
      {/* Background Gradients */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[600px] bg-blue-600/10 blur-[120px] rounded-full" />
      <div className="absolute bottom-0 right-0 w-[400px] h-[400px] bg-purple-600/5 blur-[100px] rounded-full" />

      {/* Navigation */}
      <nav className="relative z-10 max-w-7xl mx-auto px-6 py-8 flex items-center justify-between">
        <div className="flex items-center gap-2 font-black text-2xl tracking-tighter">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <Sparkles size={18} className="text-white" />
          </div>
          PromptEngine
        </div>
        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-zinc-400">
          <Link href="/pricing" className="hover:text-white transition-colors">Pricing</Link>
          <Link href="/docs" className="hover:text-white transition-colors">Documentation</Link>
          <Link href="/login" className="hover:text-white transition-colors">Sign In</Link>
          <Link href="/register">
            <Button className="bg-white text-black hover:bg-zinc-200 rounded-full px-6 py-2 h-auto text-xs font-bold">
              Get Started
            </Button>
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="relative z-10 max-w-7xl mx-auto px-6 pt-24 pb-32 flex flex-col items-center text-center">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-bold mb-8 animate-in slide-in-from-bottom-4 duration-700">
          <Zap size={14} /> Now powered by GPT-4o and Groq Llama 3
        </div>
        
        <h1 className="text-6xl md:text-8xl font-black tracking-tight mb-8 max-w-5xl leading-[0.9] animate-in slide-in-from-bottom-6 duration-1000">
          Professional <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">Prompt Engineering</span> at Scale.
        </h1>
        
        <p className="text-zinc-500 text-xl md:text-2xl max-w-2xl mb-12 animate-in slide-in-from-bottom-8 duration-1000">
          Automatically classify, enhance, and optimize your prompts using industry-standard frameworks like COSTAR and CRISPE.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 animate-in slide-in-from-bottom-10 duration-1000">
          <Link href="/register">
            <Button className="bg-blue-600 hover:bg-blue-500 text-white px-10 py-8 rounded-2xl text-lg font-bold flex items-center gap-3 shadow-2xl shadow-blue-600/20">
              Launch Dashboard <ArrowRight size={20} />
            </Button>
          </Link>
          <Link href="/pricing">
            <Button variant="outline" className="border-zinc-800 text-zinc-300 px-10 py-8 rounded-2xl text-lg font-bold hover:bg-zinc-900 transition-all">
              View Pricing
            </Button>
          </Link>
        </div>

        {/* Hero Image Mockup */}
        <div className="mt-24 w-full max-w-5xl aspect-video rounded-3xl border border-zinc-800/50 bg-zinc-900/50 backdrop-blur-3xl p-4 shadow-2xl animate-in fade-in zoom-in-95 duration-1000 delay-300">
          <div className="w-full h-full rounded-2xl bg-zinc-950/50 flex items-center justify-center border border-zinc-800/30">
            <div className="text-zinc-700 font-mono text-sm">Dashboard Preview Visualization</div>
          </div>
        </div>
      </main>

      {/* Features Grid */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 py-32 grid grid-cols-1 md:grid-cols-3 gap-12">
        <div className="space-y-4">
          <div className="w-12 h-12 bg-blue-500/10 rounded-2xl flex items-center justify-center text-blue-500">
            <Layers size={24} />
          </div>
          <h3 className="text-xl font-bold">Framework Registry</h3>
          <p className="text-zinc-500 leading-relaxed">
            Choose from COSTAR, CRISPE, RTF, and more to rewrite your prompts for maximum AI performance.
          </p>
        </div>
        <div className="space-y-4">
          <div className="w-12 h-12 bg-purple-500/10 rounded-2xl flex items-center justify-center text-purple-500">
            <Zap size={24} />
          </div>
          <h3 className="text-xl font-bold">Real-time Classification</h3>
          <p className="text-zinc-500 leading-relaxed">
            Our engine automatically detects intent and suggests the best provider like OpenAI or Groq.
          </p>
        </div>
        <div className="space-y-4">
          <div className="w-12 h-12 bg-green-500/10 rounded-2xl flex items-center justify-center text-green-500">
            <ShieldCheck size={24} />
          </div>
          <h3 className="text-xl font-bold">Enterprise Analytics</h3>
          <p className="text-zinc-500 leading-relaxed">
            Track token usage, monitor ROI, and manage team quotas with professional-grade dashboards.
          </p>
        </div>
      </section>
    </div>
  );
}
