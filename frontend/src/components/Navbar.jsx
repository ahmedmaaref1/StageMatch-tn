import React, { useState } from 'react';
import { Briefcase, Sparkles, User, Search, BarChart3, Kanban, Menu, X } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, applicationsCount = 0, student = null }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { id: 'home', label: 'Accueil', icon: null },
    { id: 'offers', label: 'Offres de Stage', icon: Search },
    { id: 'recommendations', label: 'Recommandations IA', icon: Sparkles, badge: 'IA' },
    { id: 'kanban', label: 'Candidatures', icon: Kanban, count: applicationsCount },
    { id: 'analytics', label: 'Observatoire', icon: BarChart3 },
    { id: 'profile', label: 'Mon Profil', icon: User },
  ];

  const handleNavClick = (tabId) => {
    setActiveTab(tabId);
    setMobileMenuOpen(false);
  };

  const getInitials = (name) => {
    if (!name) return 'ET';
    return name
      .split(' ')
      .map(part => part[0])
      .join('')
      .slice(0, 2)
      .toUpperCase();
  };

  return (
    <header className="bg-white/90 backdrop-blur-md border-b border-slate-200/90 sticky top-0 z-50 transition-all shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-20 items-center">
          
          {/* Logo / Brand */}
          <div 
            onClick={() => handleNavClick('home')}
            className="flex items-center gap-3.5 cursor-pointer group shrink-0"
          >
            <div className="w-11 h-11 rounded-2xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-blue-500 flex items-center justify-center text-white shadow-md shadow-blue-500/25 group-hover:scale-105 transition-all duration-200 shrink-0">
              <Briefcase className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-2xl font-black bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent tracking-tight">
                  StageMatch
                </span>
                <span className="text-xs font-black px-2 py-0.5 rounded-md bg-slate-900 text-white tracking-wide">
                  TN
                </span>
              </div>
              <span className="block text-[11px] uppercase tracking-wider text-slate-500 font-bold">
                PFE Recommender Engine
              </span>
            </div>
          </div>

          {/* Desktop Navigation Links (hidden on smaller viewports to prevent squishing) */}
          <nav className="hidden lg:flex items-center gap-1 xl:gap-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;

              return (
                <button
                  key={item.id}
                  onClick={() => handleNavClick(item.id)}
                  className={`relative flex items-center gap-2 px-3.5 py-2.5 rounded-xl text-sm font-bold whitespace-nowrap shrink-0 transition-all duration-150 ${
                    isActive
                      ? 'bg-blue-50 text-blue-600 shadow-2xs ring-1 ring-blue-500/20'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/70'
                  }`}
                >
                  {Icon && (
                    <Icon className={`w-4.5 h-4.5 shrink-0 transition-colors ${
                      isActive ? 'text-blue-600' : 'text-slate-400'
                    }`} />
                  )}
                  <span>{item.label}</span>
                  
                  {item.badge && (
                    <span className="bg-gradient-to-r from-indigo-500 to-blue-600 text-white text-[11px] font-black px-1.5 py-0.2 rounded-full shadow-2xs">
                      {item.badge}
                    </span>
                  )}

                  {item.count !== undefined && item.count > 0 && (
                    <span className="bg-blue-600 text-white text-[11px] font-bold px-2 py-0.5 rounded-full shadow-2xs animate-fade-in">
                      {item.count}
                    </span>
                  )}

                  {isActive && (
                    <span className="absolute bottom-0 left-3 right-3 h-0.5 bg-blue-600 rounded-full" />
                  )}
                </button>
              );
            })}

            {/* Quick Student Profile Indicator */}
            {student?.full_name && (
              <div 
                onClick={() => handleNavClick('profile')}
                title={`Profil connecté: ${student.full_name} (${student.university || 'ESPRIT / INSAT'})`}
                className="ml-2 pl-3 border-l border-slate-200 flex items-center gap-2.5 cursor-pointer group shrink-0"
              >
                <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-600 text-white font-black text-xs flex items-center justify-center ring-2 ring-blue-100 group-hover:ring-blue-400 transition-all shrink-0">
                  {getInitials(student.full_name)}
                </div>
                <div className="hidden 2xl:block text-left">
                  <span className="text-xs font-bold text-slate-800 block line-clamp-1 group-hover:text-blue-600">
                    {student.full_name.split(' ')[0]}
                  </span>
                  <span className="text-[11px] text-slate-400 block line-clamp-1 font-medium">
                    {student.degree_level || 'PFE'}
                  </span>
                </div>
              </div>
            )}
          </nav>

          {/* Mobile / Tablet Menu Button */}
          <div className="flex lg:hidden items-center gap-2">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2.5 rounded-2xl text-slate-700 hover:text-slate-900 hover:bg-slate-100 transition-colors border border-slate-200"
              aria-label="Menu"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

        </div>
      </div>

      {/* Mobile / Tablet Drawer Menu */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-t border-slate-200 bg-white/98 backdrop-blur-md px-5 pt-3 pb-6 space-y-2 animate-fade-in shadow-xl">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;

            return (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`w-full flex items-center justify-between px-4 py-3 rounded-2xl text-sm font-bold transition-all ${
                  isActive
                    ? 'bg-blue-50 text-blue-600 shadow-xs'
                    : 'text-slate-700 hover:bg-slate-50'
                }`}
              >
                <div className="flex items-center gap-3">
                  {Icon && <Icon className={`w-5 h-5 ${isActive ? 'text-blue-600' : 'text-slate-400'}`} />}
                  <span>{item.label}</span>
                </div>
                <div className="flex items-center gap-2">
                  {item.badge && (
                    <span className="bg-indigo-600 text-white text-[11px] font-bold px-2 py-0.5 rounded-full">
                      {item.badge}
                    </span>
                  )}
                  {item.count !== undefined && item.count > 0 && (
                    <span className="bg-blue-600 text-white text-[11px] font-bold px-2 py-0.5 rounded-full">
                      {item.count}
                    </span>
                  )}
                </div>
              </button>
            );
          })}

          {student?.full_name && (
            <div className="pt-3 border-t border-slate-100 px-3 flex items-center justify-between text-xs text-slate-500">
              <span>Connecté: <strong>{student.full_name}</strong></span>
              <span className="text-blue-600 font-bold">{student.university}</span>
            </div>
          )}
        </div>
      )}
    </header>
  );
}