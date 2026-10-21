import React, { useState, useEffect } from 'react';
import { 
  Search, 
  MapPin, 
  Building2, 
  ExternalLink, 
  Filter, 
  Sparkles, 
  RefreshCw, 
  Bookmark, 
  X, 
  ArrowUpDown,
  CheckCircle2,
  SlidersHorizontal,
  ChevronRight
} from 'lucide-react';
import { getOffers } from '../api';

const DOMAINS = [
  'Tous les domaines',
  'IA, Data & Machine Learning',
  'Web & Fullstack',
  'Backend & Microservices',
  'DevOps & Cloud',
  'Mobile Development',
  'Cybersécurité & Réseaux',
];

const CITIES = [
  'Toutes les villes',
  'Tunis (Les Berges du Lac)',
  'Tunis (El Ghazala)',
  'Ariana',
  'Sousse',
  'Sfax',
  'Tunisie',
];

const SOURCES = ['Tous', 'LinkedIn', 'Tanitjobs', 'TunisieTravail'];

export default function Offers({ 
  isSaved = () => false, 
  onToggleSave = () => {},
  initialFilters = { search: '', domain: 'Tous les domaines' },
  onResetFilters = () => {}
}) {
  const [offers, setOffers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState(initialFilters.search || '');
  const [selectedDomain, setSelectedDomain] = useState(initialFilters.domain || 'Tous les domaines');
  const [selectedCity, setSelectedCity] = useState('Toutes les villes');
  const [selectedSource, setSelectedSource] = useState('Tous');
  const [sortBy, setSortBy] = useState('recent'); // 'recent' | 'company' | 'title'
  const [showFilters, setShowFilters] = useState(false);

  // Sync when initialFilters changes (e.g. when coming from Home)
  useEffect(() => {
    if (initialFilters.search !== undefined) setSearch(initialFilters.search);
    if (initialFilters.domain) setSelectedDomain(initialFilters.domain);
  }, [initialFilters]);

  const fetchOffers = async () => {
    setLoading(true);
    try {
      const params = {};
      if (search.trim()) params.search = search.trim();
      if (selectedDomain !== 'Tous les domaines') params.domain = selectedDomain;
      if (selectedCity !== 'Toutes les villes') params.city = selectedCity;

      const data = await getOffers(params);
      setOffers(data || []);
    } catch (err) {
      console.error('Failed to load offers:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOffers();
  }, [selectedDomain, selectedCity]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchOffers();
  };

  const handleReset = () => {
    setSearch('');
    setSelectedDomain('Tous les domaines');
    setSelectedCity('Toutes les villes');
    setSelectedSource('Tous');
    setSortBy('recent');
    onResetFilters();
  };

  const handleSkillClick = (skill) => {
    setSearch(skill);
  };

  // Client-side filtering for source and sorting
  const filteredOffers = offers
    .filter(offer => {
      if (selectedSource === 'Tous') return true;
      return offer.source_site?.toLowerCase().includes(selectedSource.toLowerCase());
    })
    .sort((a, b) => {
      if (sortBy === 'company') {
        return (a.company || '').localeCompare(b.company || '');
      }
      if (sortBy === 'title') {
        return (a.title || '').localeCompare(b.title || '');
      }
      return 0; // default order from backend is already sorted
    });

  const getSourceBadgeColor = (source) => {
    switch (source?.toLowerCase()) {
      case 'linkedin':
        return 'bg-blue-50 text-blue-700 border-blue-200';
      case 'tanitjobs':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'tunisietravail':
        return 'bg-rose-50 text-rose-700 border-rose-200';
      default:
        return 'bg-slate-50 text-slate-700 border-slate-200';
    }
  };

  const hasActiveFilters = 
    search.trim() !== '' || 
    selectedDomain !== 'Tous les domaines' || 
    selectedCity !== 'Toutes les villes' || 
    selectedSource !== 'Tous';

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 pb-2 border-b border-slate-200">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-xs font-semibold mb-1">
            <Sparkles className="w-3.5 h-3.5 text-blue-600" />
            <span>Offres de Stage Vérifiées</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Catalogue des Stages PFE en Tunisie
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
            {filteredOffers.length} {filteredOffers.length > 1 ? 'opportunités disponibles' : 'opportunité disponible'} sur Tanitjobs, LinkedIn & Tunisie Travail
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="md:hidden flex items-center gap-1.5 px-3 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 text-xs font-semibold hover:bg-slate-50"
          >
            <SlidersHorizontal className="w-4 h-4 text-slate-500" />
            <span>Filtres</span>
          </button>
          
          <button
            onClick={fetchOffers}
            title="Rafraîchir les offres"
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 text-xs font-semibold hover:bg-slate-50 transition-colors shadow-2xs"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin text-blue-600' : 'text-slate-500'}`} />
            <span className="hidden sm:inline">Actualiser</span>
          </button>
        </div>
      </div>

      {/* Advanced Filter Bar */}
      <div className="bg-white rounded-3xl p-4 sm:p-5 border border-slate-200/90 shadow-xs space-y-4">
        
        {/* Main Search Row */}
        <form onSubmit={handleSearchSubmit} className="grid grid-cols-1 md:grid-cols-12 gap-3">
          
          {/* Search Keyword */}
          <div className="md:col-span-5 relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Rechercher par poste, mot-clé, tech (ex: Docker, Vermeg, IA)..."
              className="w-full pl-10 pr-9 py-2.5 rounded-xl border border-slate-200 text-xs sm:text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500 bg-slate-50/50 focus:bg-white transition-all"
            />
            {search && (
              <button
                type="button"
                onClick={() => setSearch('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>

          {/* Domain Dropdown */}
          <div className="md:col-span-4">
            <select
              value={selectedDomain}
              onChange={(e) => setSelectedDomain(e.target.value)}
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-xs sm:text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500 bg-white"
            >
              {DOMAINS.map(d => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
          </div>

          {/* Search Submit Button */}
          <div className="md:col-span-3 flex gap-2">
            <button
              type="submit"
              className="flex-1 py-2.5 px-4 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl text-xs sm:text-sm transition-colors shadow-xs flex items-center justify-center gap-1.5"
            >
              <Search className="w-4 h-4" />
              <span>Filtrer</span>
            </button>
            
            {hasActiveFilters && (
              <button
                type="button"
                onClick={handleReset}
                title="Effacer tous les filtres"
                className="px-3 py-2.5 rounded-xl border border-slate-200 text-slate-500 hover:bg-slate-50 hover:text-red-600 transition-colors text-xs font-semibold"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>

        </form>

        {/* Secondary Filter Row: City, Source, and Sort */}
        <div className="pt-2 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3 text-xs">
          
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-slate-400 font-semibold flex items-center gap-1">
              <MapPin className="w-3.5 h-3.5" /> Région :
            </span>
            <select
              value={selectedCity}
              onChange={(e) => setSelectedCity(e.target.value)}
              className="px-2.5 py-1 rounded-lg border border-slate-200 bg-white text-xs font-medium text-slate-700 focus:outline-hidden focus:ring-1 focus:ring-blue-500"
            >
              {CITIES.map(c => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>

            <span className="text-slate-300 mx-1">|</span>

            <span className="text-slate-400 font-semibold">Plateforme :</span>
            <div className="flex items-center gap-1">
              {SOURCES.map(source => (
                <button
                  key={source}
                  type="button"
                  onClick={() => setSelectedSource(source)}
                  className={`px-2 py-1 rounded-lg text-xs font-medium transition-colors ${
                    selectedSource === source
                      ? 'bg-blue-600 text-white font-semibold'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {source}
                </button>
              ))}
            </div>
          </div>

          {/* Sort By Dropdown */}
          <div className="flex items-center gap-2">
            <span className="text-slate-400 font-semibold flex items-center gap-1">
              <ArrowUpDown className="w-3.5 h-3.5" /> Trier par :
            </span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-2.5 py-1 rounded-lg border border-slate-200 bg-white text-xs font-medium text-slate-700 focus:outline-hidden focus:ring-1 focus:ring-blue-500"
            >
              <option value="recent">Plus récents</option>
              <option value="company">Entreprise (A-Z)</option>
              <option value="title">Titre du stage (A-Z)</option>
            </select>
          </div>

        </div>

        {/* Active Filters Pill Bar (if any) */}
        {hasActiveFilters && (
          <div className="pt-2 flex flex-wrap items-center gap-1.5 text-xs">
            <span className="text-[11px] text-slate-400 font-semibold">Filtres actifs :</span>
            {search && (
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200 text-[11px] font-semibold">
                Mot-clé: "{search}"
                <button onClick={() => setSearch('')} className="hover:text-blue-900"><X className="w-3 h-3" /></button>
              </span>
            )}
            {selectedDomain !== 'Tous les domaines' && (
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200 text-[11px] font-semibold">
                {selectedDomain}
                <button onClick={() => setSelectedDomain('Tous les domaines')} className="hover:text-indigo-900"><X className="w-3 h-3" /></button>
              </span>
            )}
            {selectedCity !== 'Toutes les villes' && (
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-[11px] font-semibold">
                {selectedCity}
                <button onClick={() => setSelectedCity('Toutes les villes')} className="hover:text-emerald-900"><X className="w-3 h-3" /></button>
              </span>
            )}
            {selectedSource !== 'Tous' && (
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200 text-[11px] font-semibold">
                Source: {selectedSource}
                <button onClick={() => setSelectedSource('Tous')} className="hover:text-amber-900"><X className="w-3 h-3" /></button>
              </span>
            )}
            <button
              onClick={handleReset}
              className="text-[11px] font-semibold text-slate-500 hover:text-red-600 underline ml-2"
            >
              Tout effacer
            </button>
          </div>
        )}

      </div>

      {/* Offers Grid */}
      {loading ? (
        <div className="py-20 text-center space-y-3">
          <div className="w-9 h-9 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="text-xs text-slate-500 font-medium">Recherche des stages en cours...</p>
        </div>
      ) : filteredOffers.length === 0 ? (
        <div className="py-16 text-center bg-white border border-slate-200/90 rounded-3xl p-8 space-y-4 max-w-md mx-auto shadow-xs">
          <div className="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center mx-auto">
            <Search className="w-6 h-6" />
          </div>
          <div className="space-y-1">
            <h3 className="font-bold text-slate-900 text-base">Aucune offre ne correspond à ces critères</h3>
            <p className="text-xs text-slate-500">Essayez de retirer un filtre ou de modifier votre mot-clé de recherche.</p>
          </div>
          <button
            onClick={handleReset}
            className="px-4 py-2 bg-blue-600 text-white rounded-xl text-xs font-semibold hover:bg-blue-700 transition-colors shadow-xs"
          >
            Réinitialiser les filtres
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filteredOffers.map((offer) => {
            const saved = isSaved(offer.id);
            const companyInitial = offer.company ? offer.company.trim()[0].toUpperCase() : 'E';

            return (
              <div
                key={offer.id}
                className="bg-white border border-slate-200/80 hover:border-blue-400 rounded-3xl p-5 shadow-xs hover:shadow-md transition-all flex flex-col justify-between space-y-4 group"
              >
                <div className="space-y-3">
                  
                  {/* Top Bar: Source Site & Contract */}
                  <div className="flex items-center justify-between gap-2">
                    <span className={`text-[10px] font-extrabold px-2.5 py-0.5 rounded-full border uppercase tracking-wider ${getSourceBadgeColor(offer.source_site)}`}>
                      {offer.source_site}
                    </span>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-slate-100 text-slate-600">
                      {offer.contract_type || 'Stage PFE'}
                    </span>
                  </div>

                  {/* Company & Title */}
                  <div className="space-y-1.5">
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 rounded-lg bg-gradient-to-tr from-slate-100 to-slate-200 text-slate-700 font-extrabold text-[11px] flex items-center justify-center shrink-0 border border-slate-200">
                        {companyInitial}
                      </div>
                      <span className="font-bold text-xs text-slate-700 line-clamp-1">
                        {offer.company}
                      </span>
                    </div>

                    <h3 className="font-bold text-slate-900 text-sm leading-snug line-clamp-2 group-hover:text-blue-600 transition-colors">
                      {offer.title}
                    </h3>

                    <div className="flex items-center gap-1.5 text-[11px] text-slate-500">
                      <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                      <span className="line-clamp-1">{offer.city || 'Tunisie'}</span>
                    </div>
                  </div>

                  {/* Domain Tag */}
                  <div>
                    <span className="inline-block text-[10px] font-semibold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-md border border-blue-100">
                      {offer.domain}
                    </span>
                  </div>

                  {/* Description Excerpt */}
                  <p className="text-xs text-slate-500 line-clamp-3 leading-relaxed">
                    {offer.description}
                  </p>

                  {/* Skills Tags (Clickable to filter!) */}
                  {offer.skills && offer.skills.length > 0 && (
                    <div className="flex flex-wrap gap-1 pt-1">
                      {offer.skills.slice(0, 4).map((skill) => (
                        <button
                          key={skill}
                          type="button"
                          onClick={() => handleSkillClick(skill)}
                          title={`Filtrer par ${skill}`}
                          className="text-[10px] font-semibold bg-slate-100 hover:bg-blue-100 text-slate-700 hover:text-blue-700 px-2 py-0.5 rounded-md transition-colors"
                        >
                          {skill}
                        </button>
                      ))}
                      {offer.skills.length > 4 && (
                        <span className="text-[10px] text-slate-400 font-medium px-1 py-0.5">
                          +{offer.skills.length - 4}
                        </span>
                      )}
                    </div>
                  )}
                </div>

                {/* Card Footer: Date, Bookmark & Apply Link */}
                <div className="pt-3 border-t border-slate-100 flex items-center justify-between">
                  <span className="text-[10px] text-slate-400 font-medium">
                    {offer.date_posted || 'Récent'}
                  </span>

                  <div className="flex items-center gap-2">
                    {/* Save to Kanban Bookmark Button */}
                    <button
                      onClick={() => onToggleSave(offer)}
                      title={saved ? "Retirer du CRM Kanban" : "Ajouter à mon suivi Kanban"}
                      className={`inline-flex items-center gap-1 text-[11px] font-semibold px-2.5 py-1 rounded-xl transition-all border ${
                        saved
                          ? 'bg-emerald-50 text-emerald-700 border-emerald-300 shadow-2xs'
                          : 'bg-slate-50 text-slate-600 hover:bg-slate-100 border-slate-200'
                      }`}
                    >
                      <Bookmark className={`w-3.5 h-3.5 ${saved ? 'fill-emerald-600 text-emerald-600' : 'text-slate-400'}`} />
                      <span>{saved ? 'Suivi' : 'Suivre'}</span>
                    </button>

                    {/* External Link */}
                    <a
                      href={offer.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-[11px] font-bold rounded-xl shadow-xs transition-colors"
                    >
                      <span>Postuler</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                </div>

              </div>
            );
          })}
        </div>
      )}

    </div>
  );
}