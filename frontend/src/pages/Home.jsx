import React, { useState } from 'react';
import { 
  Sparkles, 
  Search, 
  GraduationCap, 
  Building2, 
  MapPin, 
  ArrowRight, 
  CheckCircle2, 
  Layers, 
  TrendingUp, 
  Cpu, 
  Kanban,
  FileText,
  Briefcase
} from 'lucide-react';

const TOP_DOMAINS = [
  { name: 'IA & Machine Learning', domain: 'IA, Data & Machine Learning', icon: '🤖' },
  { name: 'Web & Fullstack', domain: 'Web & Fullstack', icon: '🌐' },
  { name: 'DevOps & Cloud', domain: 'DevOps & Cloud', icon: '☁️' },
  { name: 'Cybersécurité', domain: 'Cybersécurité & Réseaux', icon: '🛡️' },
  { name: 'Backend & APIs', domain: 'Backend & Microservices', icon: '⚙️' },
  { name: 'Mobile (Flutter/iOS)', domain: 'Mobile Development', icon: '📱' },
];

const FEATURED_COMPANIES = [
  { name: 'Vermeg', location: 'Tunis (Les Berges du Lac)' },
  { name: 'Orange Sofrecom', location: 'Tunis (El Ghazala)' },
  { name: 'Cynapsys (Akkodis)', location: 'Ariana' },
  { name: 'Proxym-IT', location: 'Sousse' },
  { name: 'Satoripop', location: 'Sousse' },
  { name: 'LinSoft', location: 'Tunis' },
];

export default function Home({ setActiveTab, navigateToOffers, student }) {
  const [heroSearch, setHeroSearch] = useState('');

  const handleHeroSearchSubmit = (e) => {
    e.preventDefault();
    if (navigateToOffers) {
      navigateToOffers({ search: heroSearch.trim() });
    } else {
      setActiveTab('offers');
    }
  };

  const handleDomainQuickFilter = (domainName) => {
    if (navigateToOffers) {
      navigateToOffers({ domain: domainName });
    } else {
      setActiveTab('offers');
    }
  };

  const handleCompanyQuickFilter = (companyName) => {
    if (navigateToOffers) {
      navigateToOffers({ search: companyName });
    } else {
      setActiveTab('offers');
    }
  };

  return (
    <div className="space-y-16 sm:space-y-24 py-8 sm:py-14">
      
      {/* Hero Section */}
      <section className="relative text-center max-w-6xl mx-auto px-4 sm:px-6 space-y-8 pt-2">
        
        {/* Decorative subtle background glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 sm:w-[750px] h-80 bg-gradient-to-tr from-blue-400/20 via-indigo-400/15 to-purple-400/15 rounded-full blur-3xl pointer-events-none -z-10" />

        {/* Top Tagline Badge */}
        <div className="inline-flex items-center gap-2.5 px-4 py-2 rounded-full bg-blue-50 border border-blue-200/90 text-blue-700 text-xs sm:text-sm font-bold shadow-2xs">
          <Sparkles className="w-4 h-4 text-blue-600 shrink-0" />
          <span>Plateforme IA Spéciale PFE Tunisie 2026</span>
        </div>

        {/* Main Heading */}
        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-slate-900 tracking-tight leading-[1.2]">
          Décrochez le <span className="bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-500 bg-clip-text text-transparent">Stage PFE</span> parfait selon vos compétences
        </h1>

        {/* Subtitle */}
        <p className="text-base sm:text-xl text-slate-600 max-w-3xl mx-auto leading-relaxed">
          Nous agrégeons les opportunités tech de <strong>LinkedIn, Tanitjobs et Tunisie Travail</strong>, puis comparons votre profil universitaire avec chaque offre grâce à l'IA sémantique.
        </p>

        {/* Hero Interactive Search Bar (Comfortably sized) */}
        <div className="max-w-3xl mx-auto pt-2">
          <form 
            onSubmit={handleHeroSearchSubmit}
            className="flex items-center bg-white rounded-2xl sm:rounded-3xl p-2 sm:p-2.5 border border-slate-200 shadow-xl hover:border-blue-400 focus-within:border-blue-500 focus-within:ring-4 focus-within:ring-blue-500/10 transition-all"
          >
            <div className="pl-4 pr-2 text-slate-400 shrink-0">
              <Search className="w-6 h-6" />
            </div>
            <input
              type="text"
              value={heroSearch}
              onChange={(e) => setHeroSearch(e.target.value)}
              placeholder="Rechercher un stage (ex: Docker, Spring Boot, Vermeg, IA)..."
              className="w-full py-3.5 px-2 text-base sm:text-lg text-slate-900 placeholder:text-slate-400 focus:outline-hidden bg-transparent"
            />
            <button
              type="submit"
              className="shrink-0 flex items-center gap-2 px-6 sm:px-8 py-3.5 rounded-xl sm:rounded-2xl bg-blue-600 hover:bg-blue-700 text-white text-sm sm:text-base font-bold shadow-md shadow-blue-500/20 transition-all hover:scale-[1.01]"
            >
              <span>Rechercher</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>
        </div>

        {/* Quick Domain Filter Chips */}
        <div className="flex flex-wrap items-center justify-center gap-2.5 pt-2 max-w-4xl mx-auto">
          <span className="text-xs sm:text-sm text-slate-500 font-bold mr-1">Filières clés :</span>
          {TOP_DOMAINS.map((item) => (
            <button
              key={item.domain}
              onClick={() => handleDomainQuickFilter(item.domain)}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-2xl bg-white hover:bg-blue-50 hover:text-blue-700 border border-slate-200 hover:border-blue-300 text-xs sm:text-sm font-bold text-slate-700 transition-all shadow-2xs hover:scale-[1.02]"
            >
              <span className="text-base">{item.icon}</span>
              <span>{item.name}</span>
            </button>
          ))}
        </div>

        {/* Primary Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center pt-6">
          <button
            onClick={() => setActiveTab('profile')}
            className="flex items-center justify-center gap-2.5 px-8 py-4 rounded-2xl bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-600 hover:from-blue-700 hover:to-indigo-700 text-white font-extrabold text-sm sm:text-base transition-all shadow-lg shadow-blue-500/25 hover:scale-[1.02]"
          >
            <GraduationCap className="w-5 h-5" />
            <span>{student?.full_name ? 'Mettre à jour mon profil' : 'Créer mon profil / Importer CV'}</span>
            <ArrowRight className="w-4 h-4 ml-1" />
          </button>
          
          <button
            onClick={() => setActiveTab('recommendations')}
            className="flex items-center justify-center gap-2.5 px-8 py-4 rounded-2xl bg-white border-2 border-slate-200 hover:border-indigo-400 text-slate-800 font-extrabold text-sm sm:text-base hover:bg-indigo-50/50 hover:text-indigo-700 transition-all shadow-xs hover:scale-[1.02]"
          >
            <Sparkles className="w-5 h-5 text-indigo-600" />
            <span>Voir mes recommandations IA</span>
          </button>
        </div>
      </section>

      {/* Stats Counter Bar (Prominently styled) */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 bg-white border border-slate-200/90 rounded-3xl p-6 sm:p-8 shadow-sm">
          
          <div className="flex items-center gap-4 p-4 rounded-2xl bg-slate-50 border border-slate-200/80">
            <div className="w-14 h-14 rounded-2xl bg-blue-100 text-blue-700 flex items-center justify-center shrink-0">
              <Briefcase className="w-7 h-7" />
            </div>
            <div>
              <div className="text-3xl sm:text-4xl font-black text-slate-900">58+</div>
              <div className="text-xs sm:text-sm text-slate-700 font-bold">PFE Indexés & Vérifiés</div>
              <div className="text-[11px] text-slate-400">100% liens HTTP 200 actifs</div>
            </div>
          </div>

          <div className="flex items-center gap-4 p-4 rounded-2xl bg-slate-50 border border-slate-200/80">
            <div className="w-14 h-14 rounded-2xl bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0">
              <Building2 className="w-7 h-7" />
            </div>
            <div>
              <div className="text-3xl sm:text-4xl font-black text-slate-900">37</div>
              <div className="text-xs sm:text-sm text-slate-700 font-bold">Entreprises Recruteuses</div>
              <div className="text-[11px] text-slate-400">Startups & Multinationales</div>
            </div>
          </div>

          <div className="flex items-center gap-4 p-4 rounded-2xl bg-slate-50 border border-slate-200/80">
            <div className="w-14 h-14 rounded-2xl bg-purple-100 text-purple-700 flex items-center justify-center shrink-0">
              <Sparkles className="w-7 h-7" />
            </div>
            <div>
              <div className="text-2xl sm:text-3xl font-black text-slate-900">NLP & IA</div>
              <div className="text-xs sm:text-sm text-slate-700 font-bold">Sentence-Transformers</div>
              <div className="text-[11px] text-slate-400">Similarité cosinus hybride</div>
            </div>
          </div>

          <div className="flex items-center gap-4 p-4 rounded-2xl bg-slate-50 border border-slate-200/80">
            <div className="w-14 h-14 rounded-2xl bg-amber-100 text-amber-700 flex items-center justify-center shrink-0">
              <Kanban className="w-7 h-7" />
            </div>
            <div>
              <div className="text-2xl sm:text-3xl font-black text-slate-900">CRM PFE</div>
              <div className="text-xs sm:text-sm text-slate-700 font-bold">Suivi des Entretiens</div>
              <div className="text-[11px] text-slate-400">Tableau Kanban 4 étapes</div>
            </div>
          </div>

        </div>
      </section>

      {/* Featured Tunisian Tech Employers */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-5">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-extrabold text-slate-900 flex items-center gap-2.5">
              <Building2 className="w-5 h-5 text-blue-600" />
              <span>Entreprises & PFE Books Partenaires</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-500 mt-1">Cliquez sur un recruteur pour explorer ses fiches de stage</p>
          </div>
          <button 
            onClick={() => setActiveTab('offers')}
            className="text-xs sm:text-sm font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1.5"
          >
            <span>Voir toutes les offres</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
          {FEATURED_COMPANIES.map(company => (
            <button
              key={company.name}
              onClick={() => handleCompanyQuickFilter(company.name)}
              className="p-4 rounded-2xl bg-white border border-slate-200/80 hover:border-blue-400 hover:shadow-md transition-all text-left group flex flex-col justify-between"
            >
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-xl bg-blue-50 text-blue-600 font-black text-xs flex items-center justify-center group-hover:bg-blue-600 group-hover:text-white transition-colors shrink-0">
                  {company.name[0]}
                </div>
                <span className="text-xs sm:text-sm font-bold text-slate-900 group-hover:text-blue-600 transition-colors line-clamp-1">
                  {company.name}
                </span>
              </div>
              <span className="text-[11px] text-slate-400 mt-2.5 block line-clamp-1 font-medium">
                {company.location.split('(')[0]}
              </span>
            </button>
          ))}
        </div>
      </section>

      {/* How it Works Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        <div className="text-center space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-slate-100 text-slate-700 text-xs sm:text-sm font-bold">
            <Layers className="w-4 h-4 text-blue-600" />
            <span>Fonctionnement de StageMatch TN</span>
          </div>
          <h2 className="text-2xl sm:text-3xl lg:text-4xl font-black text-slate-900">
            Un matching algorithmique transparent en 3 étapes
          </h2>
          <p className="text-slate-500 text-sm sm:text-base max-w-2xl mx-auto">
            Conçu sur-mesure pour les universités tunisiennes (INSAT, ESPRIT, ENIT, ISI, FST, SUP'COM, ENSI...).
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <div className="bg-white border border-slate-200/90 rounded-3xl p-7 space-y-4 shadow-2xs hover:shadow-md transition-shadow">
            <div className="w-14 h-14 rounded-2xl bg-blue-50 text-blue-600 font-black flex items-center justify-center text-xl">
              1
            </div>
            <div className="space-y-2">
              <h3 className="font-extrabold text-slate-900 text-lg">Remplissez ou Importez votre CV</h3>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                Notre parseur intelligent extrait automatiquement votre université, filière et compétences depuis votre CV PDF en quelques secondes.
              </p>
            </div>
          </div>

          <div className="bg-white border border-slate-200/90 rounded-3xl p-7 space-y-4 shadow-2xs hover:shadow-md transition-shadow">
            <div className="w-14 h-14 rounded-2xl bg-indigo-50 text-indigo-600 font-black flex items-center justify-center text-xl">
              2
            </div>
            <div className="space-y-2">
              <h3 className="font-extrabold text-slate-900 text-lg">Analyse des Écarts de Compétences</h3>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                L'IA calcule le score de compatibilité cosinus et vous indique exactement les compétences acquises et les technologies manquantes pour réussir l'entretien.
              </p>
            </div>
          </div>

          <div className="bg-white border border-slate-200/90 rounded-3xl p-7 space-y-4 shadow-2xs hover:shadow-md transition-shadow">
            <div className="w-14 h-14 rounded-2xl bg-emerald-50 text-emerald-600 font-black flex items-center justify-center text-xl">
              3
            </div>
            <div className="space-y-2">
              <h3 className="font-extrabold text-slate-900 text-lg">Pilotez votre Pipeline Kanban</h3>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                Suivez vos candidatures envoyées, planifiez vos entretiens techniques et gardez des notes pour chaque entreprise jusqu'à l'offre finale.
              </p>
            </div>
          </div>

        </div>
      </section>

    </div>
  );
}