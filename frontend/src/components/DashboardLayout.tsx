"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { 
  LayoutDashboard, 
  History, 
  Settings, 
  LogOut, 
  ChevronLeft, 
  ChevronRight,
  Sparkles
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface SidebarItemProps {
  href: string;
  icon: React.ReactNode;
  label: string;
  active?: boolean;
  collapsed?: boolean;
}

const SidebarItem = ({ href, icon, label, active, collapsed }: SidebarItemProps) => {
  return (
    <Link 
      href={href}
      className={cn(
        "flex items-center gap-3 px-3 py-2 rounded-lg transition-all duration-200 group",
        active 
          ? "bg-zinc-800 text-white shadow-lg shadow-black/20" 
          : "text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800/50"
      )}
    >
      <div className={cn("flex-shrink-0", active ? "text-blue-400" : "group-hover:text-blue-400")}>
        {icon}
      </div>
      {!collapsed && <span className="font-medium text-sm">{label}</span>}
    </Link>
  );
};

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [collapsed, setCollapsed] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    router.push("/login");
  };

  return (
    <div className="flex min-h-screen bg-zinc-950 text-zinc-100 bg-grid">
      {/* Sidebar */}
      <aside 
        className={cn(
          "fixed left-0 top-0 h-full glass border-r border-zinc-800/50 transition-all duration-300 z-50",
          collapsed ? "w-20" : "w-64"
        )}
      >
        <div className="flex flex-col h-full p-4">
          <div className="flex items-center justify-between mb-8 px-2">
            {!collapsed && (
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center">
                  <Sparkles size={20} className="text-white" />
                </div>
                <span className="font-bold text-xl tracking-tight">PromptEngine</span>
              </div>
            )}
            {collapsed && (
              <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center mx-auto">
                <Sparkles size={20} className="text-white" />
              </div>
            )}
          </div>

          <nav className="flex-1 space-y-2">
            <SidebarItem 
              href="/dashboard" 
              icon={<LayoutDashboard size={20} />} 
              label="Prompt Editor" 
              active={pathname === "/dashboard"}
              collapsed={collapsed}
            />
            <SidebarItem 
              href="/dashboard/history" 
              icon={<History size={20} />} 
              label="Enhancement History" 
              active={pathname === "/dashboard/history"}
              collapsed={collapsed}
            />
            <SidebarItem 
              href="/dashboard/settings" 
              icon={<Settings size={20} />} 
              label="Settings" 
              active={pathname === "/dashboard/settings"}
              collapsed={collapsed}
            />
          </nav>

          <div className="mt-auto pt-4 border-t border-zinc-800/50">
            <button 
              onClick={() => setCollapsed(!collapsed)}
              className="flex items-center gap-3 w-full px-3 py-2 text-zinc-400 hover:text-zinc-100 transition-colors mb-2"
            >
              {collapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
              {!collapsed && <span className="text-sm font-medium">Collapse Sidebar</span>}
            </button>
            <Button 
              onClick={handleLogout}
              variant="ghost" 
              className={cn(
                "w-full justify-start gap-3 text-zinc-400 hover:text-red-400 hover:bg-red-500/10",
                collapsed ? "px-2" : "px-3"
              )}
            >
              <LogOut size={20} />
              {!collapsed && <span className="text-sm font-medium">Logout</span>}
            </Button>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className={cn(
        "flex-1 transition-all duration-300 p-8",
        collapsed ? "ml-20" : "ml-64"
      )}>
        <div className="max-w-6xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}
