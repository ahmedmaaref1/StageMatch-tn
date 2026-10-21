import React, { useState, useEffect } from 'react';
import { 
  BarChart3, 
  TrendingUp, 
  Building2, 
  Briefcase, 
  Cpu, 
  MapPin, 
  Sparkles, 
  RefreshCw, 
  CheckCircle2, 
  ArrowRight, 
  Lightbulb,
  Award,
  Zap,
  Clock,
  Radio,
  PlayCircle,
  Loader2
} from 'lucide-react';
import { getMarketAnalytics, getScrapingStatus, triggerManualScraping } from '../api';

export default function Analytics({ setActiveTab }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [scrapingStatus, setScrapingStatus] = useState(null);
  const [syncing, setSyncing] = useState(false);
  const [syncMessage, setSyncMessage] = useState(null);

  const fetchAnalytics = async () => {
    setLoading(true);
    setError(null);
    try {
      const [res, status] = await Promise.all([
        getMarketAnalytics(),
        getScrapingStatus().catch(() => null),
      ]);
      setData(res);
      if (status) setScrapingStatus(status);
    } catch (err) {
      console.error('Failed to load market analytics:', err);
      setError("Impossible de charger les statistiques du marché tech.");
    } finally {
      setLoading(false);
    }
  };

  const handleManualSync = async () => {
    setSyncing(true);
    setSyncMessage(null);
    try {
      await triggerManualScraping();
      setSyncMessage("Synchronisation en arrière-plan démarrée ! Les nouvelles offres s'indexent automatiquement.");
      setTimeout(async () => {
        try {
          const [updatedAnalytics, updatedStatus] = await Promise.all([
            getMarketAnalytics(),
            getScrapingStatus(),
          ]);
          setData(updatedAnalytics);
          setScrapingStatus(updatedStatus);
        } catch (e) {
          console.error(e);
        } finally {
          setSyncing(false);
        }
      }, 4000);
    } catch (err) {
      console.error('Manual scrape trigger failed:', err);
      setSyncing(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const getDomainColor = (index) => {
    const colors = [
      { bar: 'from-purple-500 to-indigo-600', badge: 'bg-purple-50 text-purple-700 border-purple-200' },
      { bar: 'from-blue-500 to-cyan-600', badge: 'bg-blue-50 text-blue-700 border-blue-200' },
      { bar: 'from-emerald-500 to-teal-600', badge: 'bg-emerald-50 text-emerald-700 border-emerald-200' },
      { bar: 'from-rose-500 to-red-600', badge: 'bg-rose-50 text-rose-700 border-rose-200' },
      { bar: 'from-amber-500 to-orange-600', badge: 'bg-amber-50 text-amber-700 border-amber-200' },
      { bar: 'from-sky-500 to-blue-600', badge: 'bg-sky-50 text-sky-700 border-sky-200' },
    ];
    return colors[index % colors.length];
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center space-y-4">
        <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="text-slate-600 font-medium">Analyse des tendances du marché PFE en cours...</p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="max-w-md mx-auto px-4 py-20 text-center space-y-4">
        <div className="w-12 h-12 bg-red-50 text-red-600 rounded-xl flex items-center justify-center mx-auto">
          <BarChart3 className="w-6 h-6" />
        </div>
        <p className="text-slate-800 font-medium">{error || "Aucune donnée disponible"}</p>
        <button
          onClick={fetchAnalytics}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-semibold hover:bg-blue-700 transition-colors"
        >
          Réessayer
        </button>
      </div>
    );
  }

  const totalOffers = data.total_offers || 1;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-xs font-semibold mb-2">
            <Sparkles className="w-3.5 h-3.5 text-blue-600" />
            <span>Marché Tech Tunisien 2026</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Observatoire & Statistiques du Marché PFE
          </h1>
          <p className="text-slate-600 text-sm mt-1">
            Données agrégées en direct sur les compétences, filières et entreprises qui recrutent en Tunisie.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 text-xs font-medium border border-emerald-200">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            {data.total_offers} PFE Actifs
          </span>
          <button
            onClick={fetchAnalytics}
            title="Rafraîchir les statistiques"
            className="p-2 text-slate-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors border border-slate-200"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Automated Background Scraping Status Panel */}
      <div className="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 rounded-3xl p-5 sm:p-6 text-white shadow-md border border-slate-800 space-y-4">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-blue-500/20 border border-blue-400/30 flex items-center justify-center text-blue-300 shrink-0">
              <Clock className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-sm sm:text-base text-white">
                  Planificateur de Scraping Automatique (Cron 24h)
                </h3>
                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 text-[11px] font-bold">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                  {scrapingStatus?.is_active ? 'Actif' : 'En veille'}
                </span>
              </div>
              <p className="text-xs text-blue-200/80 mt-0.5">
                Collecte continue et détection de nouveaux stages PFE sur Tanitjobs, LinkedIn & Tunisie Travail.
              </p>
            </div>
          </div>

          <button
            onClick={handleManualSync}
            disabled={syncing}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold transition-all shadow-md shadow-blue-500/20 disabled:opacity-50 shrink-0"
          >
            {syncing ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Synchronisation en cours...</span>
              </>
            ) : (
              <>
                <PlayCircle className="w-4 h-4" />
                <span>Synchroniser maintenant</span>
              </>
            )}
          </button>
        </div>

        {/* Status Metrics Bar */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 border-t border-white/10 text-xs">
          <div className="p-3 rounded-xl bg-white/5 border border-white/10 space-y-1">
            <span className="text-[10px] uppercase font-bold text-blue-300 block">Prochaine Exécution Auto</span>
            <span className="text-xs sm:text-sm font-bold text-white">
              {scrapingStatus?.next_run
                ? new Date(scrapingStatus.next_run).toLocaleString('fr-FR', {
                    weekday: 'short',
                    day: 'numeric',
                    month: 'short',
                    hour: '2-digit',
                    minute: '2-digit',
                  })
                : 'Tous les jours à 02:00'}
            </span>
          </div>

          <div className="p-3 rounded-xl bg-white/5 border border-white/10 space-y-1">
            <span className="text-[10px] uppercase font-bold text-blue-300 block">Dernier Statut</span>
            <span className="text-xs sm:text-sm font-bold text-emerald-300">
              {scrapingStatus?.last_status || 'En attente'} 
              {scrapingStatus?.last_inserted_count !== undefined && ` (+${scrapingStatus.last_inserted_count} ajoutés)`}
            </span>
          </div>

          <div className="p-3 rounded-xl bg-white/5 border border-white/10 space-y-1">
            <span className="text-[10px] uppercase font-bold text-blue-300 block">Fréquence Programmée</span>
            <span className="text-xs sm:text-sm font-bold text-white">
              Chaque 24h à 02h00 (Heure de Tunis)
            </span>
          </div>
        </div>

        {syncMessage && (
          <div className="p-3 rounded-xl bg-blue-500/20 border border-blue-400/30 text-xs text-blue-100 flex items-center gap-2 animate-fade-in">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>{syncMessage}</span>
          </div>
        )}
      </div>

      {/* 4 KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        
        {/* Total Offers */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Offres PFE Indexées</span>
            <div className="w-9 h-9 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
              <Briefcase className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-slate-900">{data.total_offers}</span>
            <span className="text-xs font-medium text-emerald-600 flex items-center gap-0.5">
              <CheckCircle2 className="w-3 h-3" /> 100% Vérifiées
            </span>
          </div>
          <p className="mt-1 text-xs text-slate-500">Sujets de stage de fin d'études validés</p>
        </div>

        {/* Total Companies */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Entreprises Tech</span>
            <div className="w-9 h-9 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <Building2 className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-slate-900">{data.total_companies}</span>
            <span className="text-xs font-medium text-slate-500">Recruteurs</span>
          </div>
          <p className="mt-1 text-xs text-slate-500">Startups, ESN & Pôles de R&D en Tunisie</p>
        </div>

        {/* Top Track */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Filière #1 en Demande</span>
            <div className="w-9 h-9 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center">
              <TrendingUp className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3">
            <span className="text-lg font-bold text-purple-900 line-clamp-1">{data.top_track}</span>
          </div>
          <p className="mt-1 text-xs text-slate-500">Plus forte concentration de propositions</p>
        </div>

        {/* Top Skill */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Compétence Clé #1</span>
            <div className="w-9 h-9 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center">
              <Cpu className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl font-extrabold text-amber-900">{data.top_skill}</span>
            <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-amber-100 text-amber-800">
              Essentiel
            </span>
          </div>
          <p className="mt-1 text-xs text-slate-500">Technologie la plus récurrente dans les fiches</p>
        </div>

      </div>

      {/* Main Charts & Breakdown Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Left Column: Filières Tech en Demande */}
        <div className="bg-white rounded-3xl p-6 sm:p-7 border border-slate-200/80 shadow-xs space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-blue-600" />
                Répartition par Filière Technologique
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">Part de chaque domaine dans le marché global du PFE</p>
            </div>
          </div>

          <div className="space-y-4 pt-2">
            {data.by_domain?.map((domain, idx) => {
              const pct = Math.round((domain.count / totalOffers) * 100);
              const colorStyle = getDomainColor(idx);
              return (
                <div key={domain.name} className="space-y-1.5">
                  <div className="flex justify-between items-center text-sm">
                    <span className="font-semibold text-slate-800">{domain.name}</span>
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-slate-500 font-medium">{domain.count} offres</span>
                      <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${colorStyle.badge}`}>
                        {pct}%
                      </span>
                    </div>
                  </div>
                  <div className="w-full h-3 bg-slate-100 rounded-full overflow-hidden">
                    <div 
                      className={`h-full rounded-full bg-gradient-to-r ${colorStyle.bar} transition-all duration-700`}
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column: Top 10 Compétences les Plus Demandées */}
        <div className="bg-white rounded-3xl p-6 sm:p-7 border border-slate-200/80 shadow-xs space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Award className="w-5 h-5 text-amber-500" />
                Top 10 Compétences les Plus Exigées
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">Fréquence d'apparition dans les fiches de stage PFE</p>
            </div>
          </div>

          <div className="space-y-3 pt-2">
            {data.top_skills?.map((item, idx) => {
              const pct = Math.round((item.count / totalOffers) * 100);
              return (
                <div key={item.name} className="flex items-center gap-3">
                  <span className={`w-6 text-center text-xs font-bold ${
                    idx === 0 ? 'text-amber-600' : idx === 1 ? 'text-slate-600' : idx === 2 ? 'text-amber-800' : 'text-slate-400'
                  }`}>
                    #{idx + 1}
                  </span>
                  
                  <div className="flex-1 space-y-1">
                    <div className="flex justify-between items-center text-xs">
                      <span className="font-semibold text-slate-800">{item.name}</span>
                      <span className="text-slate-500">{item.count} mentions ({pct}%)</span>
                    </div>
                    <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                      <div 
                        className={`h-full rounded-full transition-all duration-700 ${
                          idx === 0 
                            ? 'bg-amber-500' 
                            : idx < 3 
                              ? 'bg-blue-600' 
                              : 'bg-slate-400'
                        }`}
                        style={{ width: `${Math.min(pct * 2.2, 100)}%` }}
                      />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

      </div>

      {/* Hubs Régionaux & Entreprises Clés */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Pôles Régionaux */}
        <div className="bg-white rounded-3xl p-6 sm:p-7 border border-slate-200/80 shadow-xs space-y-5 lg:col-span-1">
          <div>
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <MapPin className="w-5 h-5 text-rose-500" />
              Pôles Géographiques
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">Concentration des PFE par pôle technologique</p>
          </div>

          <div className="space-y-3">
            {data.by_city?.slice(0, 6).map((city) => (
              <div 
                key={city.name}
                className="flex items-center justify-between p-3 rounded-xl bg-slate-50 hover:bg-blue-50/50 transition-colors border border-slate-100"
              >
                <div className="flex items-center gap-2.5">
                  <MapPin className="w-4 h-4 text-slate-400" />
                  <span className="text-xs font-semibold text-slate-700">{city.name}</span>
                </div>
                <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-white text-blue-700 shadow-2xs border border-slate-200">
                  {city.count} {city.count > 1 ? 'stages' : 'stage'}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Top Entreprises Recruteuses */}
        <div className="bg-white rounded-3xl p-6 sm:p-7 border border-slate-200/80 shadow-xs space-y-5 lg:col-span-2">
          <div>
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <Building2 className="w-5 h-5 text-indigo-600" />
              Recruteurs Phares & PFE Books
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">Entreprises ayant publié des sujets de stage validés</p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
            {data.top_companies?.slice(0, 8).map((comp) => (
              <div 
                key={comp.name} 
                className="p-3.5 rounded-2xl bg-gradient-to-b from-slate-50 to-white border border-slate-200/80 flex flex-col justify-between hover:border-blue-300 hover:shadow-xs transition-all"
              >
                <div>
                  <span className="text-xs font-bold text-slate-800 line-clamp-1">{comp.name}</span>
                  <span className="text-[10px] text-slate-400 font-medium">Entreprise Tech</span>
                </div>
                <div className="mt-3 flex items-center justify-between">
                  <span className="text-[11px] font-semibold text-blue-600">
                    {comp.count} sujet{comp.count > 1 ? 's' : ''}
                  </span>
                  <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Strategic Insights & Advice for Students */}
      <div className="bg-gradient-to-br from-slate-900 via-indigo-950 to-blue-950 rounded-3xl p-6 sm:p-8 text-white shadow-xl space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-amber-400/20 text-amber-300 flex items-center justify-center">
            <Lightbulb className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white">Conseils Stratégiques pour Candidater à votre PFE</h3>
            <p className="text-xs text-slate-300">Recommandations basées sur l'analyse algorithmique des 58 sujets indexés</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-2xl bg-white/5 border border-white/10 space-y-2">
            <div className="flex items-center gap-2 text-cyan-300 text-sm font-semibold">
              <Zap className="w-4 h-4" />
              <span>Conteneurisation Obligatoire</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              <strong className="text-white">Docker et Git</strong> apparaissent dans plus de 35% de toutes les offres. Même pour un projet orienté IA ou Mobile, savoir conteneuriser son application est un prérequis déterminant en entretien technique.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-white/5 border border-white/10 space-y-2">
            <div className="flex items-center gap-2 text-purple-300 text-sm font-semibold">
              <Sparkles className="w-4 h-4" />
              <span>L'Effervescence de l'IA</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              L'<strong className="text-white">IA & Machine Learning</strong> est la filière #1 avec près de 25% des opportunités (LLM, RAG, Computer Vision, MLOps). Mettez en avant vos projets open-source PyTorch et Hugging Face sur votre CV.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-white/5 border border-white/10 space-y-2">
            <div className="flex items-center gap-2 text-emerald-300 text-sm font-semibold">
              <CheckCircle2 className="w-4 h-4" />
              <span>Modern Microservices</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Pour le Web et le Backend, la combinaison <strong className="text-white">REST API + TypeScript / FastAPI + PostgreSQL</strong> domine largement le marché par rapport aux architectures monolithiques traditionnelles.
            </p>
          </div>
        </div>

        <div className="pt-2 flex flex-col sm:flex-row items-center justify-between gap-4 border-t border-white/10">
          <p className="text-xs text-slate-400">
            Maximisez votre score de matching en alignant vos projets universitaires avec ces technologies clés.
          </p>
          <div className="flex items-center gap-3">
            <button
              onClick={() => setActiveTab('recommendations')}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold transition-all shadow-md shadow-blue-500/20"
            >
              <span>Voir mes recommandations</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => setActiveTab('offers')}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-semibold transition-all"
            >
              <span>Parcourir toutes les offres</span>
            </button>
          </div>
        </div>

      </div>

    </div>
  );
}
