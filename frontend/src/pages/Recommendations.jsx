import React, { useState, useEffect } from 'react';
import { 
  Sparkles, 
  Building2, 
  MapPin, 
  ExternalLink, 
  GraduationCap, 
  ArrowRight, 
  CheckCircle2, 
  User, 
  Bookmark,
  Search,
  Filter,
  SlidersHorizontal,
  Lightbulb,
  Award,
  Zap,
  TrendingUp,
  X
} from 'lucide-react';
import { getRecommendations } from '../api';

export default function Recommendations({ 
  student, 
  setActiveTab, 
  isSaved = () => false, 
  onToggleSave = () => {} 
}) {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [minScore, setMinScore] = useState(0); // 0, 65, 80
  const [selectedDomain, setSelectedDomain] = useState('Tous');

  useEffect(() => {
    if (student?.id) {
      loadRecommendations(student.id);
    }
  }, [student]);

  const loadRecommendations = async (studentId) => {
    setLoading(true);
    setError(null);
    try {
      const data = await getRecommendations(studentId, 20);
      setRecommendations(data.recommendations || []);
    } catch (err) {
      console.error(err);
      setError("Impossible de charger les recommandations. Vérifiez que votre backend est démarré.");
    } finally {
      setLoading(false);
    }
  };

  // If student profile not created yet, prompt them to create it!
  if (!student?.id) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-20 text-center space-y-6">
        <div className="w-16 h-16 rounded-3xl bg-blue-50 text-blue-600 flex items-center justify-center mx-auto shadow-xs border border-blue-100">
          <User className="w-8 h-8" />
        </div>
        <div className="space-y-2">
          <h2 className="text-2xl font-bold text-slate-900">
            Complétez d'abord votre profil étudiant
          </h2>
          <p className="text-slate-600 text-sm max-w-md mx-auto leading-relaxed">
            Pour que notre modèle d'IA sémantique puisse calculer votre compatibilité avec les 58+ offres en Tunisie, renseignez votre université, filière et compétences.
          </p>
        </div>
        <button
          onClick={() => setActiveTab('profile')}
          className="inline-flex items-center gap-2 px-6 py-3.5 rounded-2xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold text-sm hover:from-blue-700 hover:to-indigo-700 transition-all shadow-md shadow-blue-500/25 hover:scale-[1.01]"
        >
          <span>Créer mon profil / Importer CV</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    );
  }

  // Calculate distinct domains present in the student's recommendations
  const distinctDomains = ['Tous', ...Array.from(new Set(recommendations.map(r => r.offer?.domain).filter(Boolean)))];

  // Filtering recommendations
  const filteredRecs = recommendations.filter(item => {
    const offer = item.offer;
    if (!offer) return false;

    // Filter by min score
    if (item.match_score < minScore) return false;

    // Filter by domain
    if (selectedDomain !== 'Tous' && offer.domain !== selectedDomain) return false;

    // Filter by search keyword
    if (searchTerm.trim()) {
      const q = searchTerm.toLowerCase();
      const inTitle = offer.title?.toLowerCase().includes(q);
      const inCompany = offer.company?.toLowerCase().includes(q);
      const inSkills = offer.skills?.some(s => s.toLowerCase().includes(q));
      if (!inTitle && !inCompany && !inSkills) return false;
    }

    return true;
  });

  // Score statistics
  const topScore = recommendations.length > 0 ? Math.round(recommendations[0].match_score) : 0;
  const avgScore = recommendations.length > 0 
    ? Math.round(recommendations.reduce((acc, curr) => acc + curr.match_score, 0) / recommendations.length)
    : 0;

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Student Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-blue-950 rounded-3xl p-6 sm:p-8 text-white shadow-xl flex flex-col md:flex-row justify-between items-start md:items-center gap-6 border border-slate-800">
        <div className="space-y-2.5">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 text-xs font-bold border border-blue-400/20">
            <Sparkles className="w-3.5 h-3.5 text-blue-300" />
            <span>Recommandation Personnalisée par NLP & IA</span>
          </div>
          
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Bonjour, {student.full_name} 👋
          </h1>
          
          <p className="text-xs sm:text-sm text-blue-200">
            {student.degree_level} en <strong className="text-white">{student.domain}</strong> • {student.university}
          </p>

          <div className="flex flex-wrap gap-1.5 pt-1">
            {student.skills?.map(skill => (
              <span key={skill} className="px-2.5 py-0.5 rounded-lg bg-white/10 text-xs font-medium text-white border border-white/15">
                {skill}
              </span>
            ))}
          </div>
        </div>

        {/* Quick Stats Pill & Edit Profile button */}
        <div className="flex flex-col sm:flex-row md:flex-col items-start md:items-end gap-3 shrink-0">
          <div className="flex items-center gap-3 bg-white/10 backdrop-blur-md px-4 py-2.5 rounded-2xl border border-white/15">
            <div className="text-left md:text-right">
              <span className="text-[10px] uppercase font-bold text-blue-200 block">Meilleur Match</span>
              <span className="text-2xl font-black text-amber-300">{topScore}%</span>
            </div>
            <div className="h-8 w-px bg-white/20" />
            <div className="text-left md:text-right">
              <span className="text-[10px] uppercase font-bold text-blue-200 block">Moyenne</span>
              <span className="text-2xl font-black text-white">{avgScore}%</span>
            </div>
          </div>

          <button
            onClick={() => setActiveTab('profile')}
            className="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-bold border border-white/20 transition-colors"
          >
            Modifier mes compétences
          </button>
        </div>
      </div>

      {/* Filter Toolbar for Recommendations */}
      <div className="bg-white rounded-3xl p-4 sm:p-5 border border-slate-200/90 shadow-xs space-y-3">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
          <div>
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-indigo-600" />
              <span>{filteredRecs.length} Offres les Plus Compatibles</span>
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Classement hybride combinant similarité sémantique (descriptions) et analyse des compétences
            </p>
          </div>

          {/* Search inside recommendations */}
          <div className="relative w-full sm:w-64">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Rechercher dans mes matchs..."
              className="w-full pl-9 pr-7 py-2 rounded-xl border border-slate-200 text-xs focus:outline-hidden focus:ring-2 focus:ring-blue-500 bg-slate-50 focus:bg-white"
            />
            {searchTerm && (
              <button 
                onClick={() => setSearchTerm('')}
                className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
              >
                <X className="w-3 h-3" />
              </button>
            )}
          </div>
        </div>

        {/* Filter Pills: Score Threshold & Domains */}
        <div className="pt-2 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3 text-xs">
          
          <div className="flex flex-wrap items-center gap-1.5">
            <span className="text-slate-400 font-semibold mr-1">Seuil de match :</span>
            {[
              { label: 'Tous les scores', val: 0 },
              { label: '≥ 60% Bon Match', val: 60 },
              { label: '≥ 75% Top Match 🥇', val: 75 },
            ].map(scoreOpt => (
              <button
                key={scoreOpt.val}
                onClick={() => setMinScore(scoreOpt.val)}
                className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition-colors ${
                  minScore === scoreOpt.val
                    ? 'bg-indigo-600 text-white'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {scoreOpt.label}
              </button>
            ))}
          </div>

          {distinctDomains.length > 2 && (
            <div className="flex items-center gap-1.5">
              <span className="text-slate-400 font-semibold">Filière :</span>
              <select
                value={selectedDomain}
                onChange={(e) => setSelectedDomain(e.target.value)}
                className="px-2.5 py-1 rounded-lg border border-slate-200 bg-white text-xs font-semibold text-slate-700 focus:outline-hidden"
              >
                {distinctDomains.map(d => (
                  <option key={d} value={d}>{d}</option>
                ))}
              </select>
            </div>
          )}

        </div>
      </div>

      {/* Main Results */}
      {loading ? (
        <div className="py-20 text-center space-y-3">
          <div className="w-9 h-9 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="text-xs text-slate-500 font-medium">Calcul des embeddings et similarités cosinus...</p>
        </div>
      ) : error ? (
        <div className="p-6 bg-red-50 border border-red-200 rounded-3xl text-red-700 text-xs sm:text-sm text-center">
          {error}
        </div>
      ) : filteredRecs.length === 0 ? (
        <div className="py-16 text-center bg-white border border-slate-200/90 rounded-3xl p-8 space-y-3 max-w-md mx-auto">
          <Sparkles className="w-10 h-10 text-slate-300 mx-auto" />
          <h3 className="font-bold text-slate-800 text-sm">Aucun résultat pour ces filtres</h3>
          <p className="text-xs text-slate-500">Essayez de baisser le seuil de match ou de vider la recherche.</p>
          <button
            onClick={() => { setSearchTerm(''); setMinScore(0); setSelectedDomain('Tous'); }}
            className="px-4 py-2 bg-indigo-600 text-white rounded-xl text-xs font-semibold hover:bg-indigo-700"
          >
            Réinitialiser les filtres
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredRecs.map((item, index) => {
            const offer = item.offer;
            const isTop = index === 0 && minScore === 0 && !searchTerm && selectedDomain === 'Tous';
            const saved = isSaved(offer.id);
            const score = Math.round(item.match_score);

            return (
              <div
                key={offer.id}
                className={`bg-white border rounded-3xl p-6 shadow-xs hover:shadow-md transition-all flex flex-col md:flex-row justify-between items-start md:items-center gap-6 ${
                  isTop ? 'border-indigo-400 ring-2 ring-indigo-500/15' : 'border-slate-200/90'
                }`}
              >
                <div className="space-y-3 flex-1">
                  
                  {/* Top Badges */}
                  <div className="flex flex-wrap items-center gap-2">
                    {isTop && (
                      <span className="text-[11px] font-extrabold px-3 py-0.5 rounded-full bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-xs">
                        🥇 Meilleur Match IA
                      </span>
                    )}
                    <span className="text-xs font-bold px-2.5 py-0.5 rounded-md bg-blue-50 text-blue-700 border border-blue-100">
                      {offer.domain}
                    </span>
                    <span className="text-xs text-slate-400 font-medium">
                      via {offer.source_site}
                    </span>
                  </div>

                  {/* Job Title and Company */}
                  <div>
                    <h3 className="text-base sm:text-lg font-bold text-slate-900 hover:text-blue-600 transition-colors">
                      {offer.title}
                    </h3>
                    <div className="flex items-center gap-2 text-xs text-slate-500 mt-1">
                      <Building2 className="w-3.5 h-3.5 text-slate-400" />
                      <span className="font-bold text-slate-700">{offer.company}</span>
                      <span>•</span>
                      <MapPin className="w-3.5 h-3.5 text-slate-400" />
                      <span>{offer.city}</span>
                    </div>
                  </div>

                  {/* Skills Breakdown: Acquired vs Gap */}
                  <div className="space-y-2 pt-1 text-xs">
                    
                    {/* Acquired Skills */}
                    <div className="flex flex-wrap items-center gap-1.5">
                      <span className="text-slate-500 font-semibold mr-1">Compétences acquises :</span>
                      {item.matching_skills && item.matching_skills.length > 0 ? (
                        item.matching_skills.map(s => (
                          <span key={s} className="inline-flex items-center gap-1 text-[11px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200 px-2 py-0.5 rounded-md">
                            <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                            {s}
                          </span>
                        ))
                      ) : (
                        <span className="text-[11px] text-slate-400 italic">Aucune correspondance directe</span>
                      )}
                    </div>

                    {/* Skill Gap (Technologies to learn) */}
                    {item.missing_skills && item.missing_skills.length > 0 && (
                      <div className="flex flex-wrap items-center gap-1.5">
                        <span className="text-amber-800 font-semibold mr-1">À développer pour ce PFE :</span>
                        {item.missing_skills.map(s => (
                          <span key={s} className="inline-flex items-center gap-1 text-[11px] font-bold bg-amber-50 text-amber-800 border border-amber-200/80 px-2 py-0.5 rounded-md">
                            <span className="text-amber-500 font-black">+</span>
                            {s}
                          </span>
                        ))}
                      </div>
                    )}

                    {/* AI Career Advice Tip */}
                    {item.match_reason && (
                      <div className="mt-2 text-xs text-slate-600 bg-slate-50 border border-slate-200/80 rounded-2xl px-3.5 py-2.5 flex items-start gap-2.5">
                        <span className="text-indigo-600 font-bold text-sm leading-none shrink-0 mt-0.5">💡</span>
                        <span className="leading-relaxed">{item.match_reason}</span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Right Column: Score & Action Buttons */}
                <div className="flex md:flex-col items-center md:items-end justify-between w-full md:w-auto gap-4 shrink-0 pt-4 md:pt-0 border-t md:border-t-0 border-slate-100">
                  <div className="text-left md:text-right">
                    <div className="text-3xl font-black bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent">
                      {score}%
                    </div>
                    <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">
                      Score de Match
                    </span>
                  </div>

                  <div className="flex flex-col sm:flex-row md:flex-col gap-2 w-full md:w-auto">
                    {/* Bookmark to Kanban Button */}
                    <button
                      onClick={() => onToggleSave(offer)}
                      title={saved ? "Retirer du suivi Kanban" : "Ajouter à mes candidatures"}
                      className={`inline-flex items-center justify-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold transition-all border ${
                        saved
                          ? 'bg-emerald-50 text-emerald-700 border-emerald-300 shadow-2xs'
                          : 'bg-slate-50 text-slate-700 hover:bg-slate-100 border-slate-200'
                      }`}
                    >
                      <Bookmark className={`w-3.5 h-3.5 ${saved ? 'fill-emerald-600 text-emerald-600' : 'text-slate-400'}`} />
                      <span>{saved ? 'Suivi' : 'Suivre ce PFE'}</span>
                    </button>

                    {/* Apply Button */}
                    <a
                      href={offer.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold shadow-xs transition-colors"
                    >
                      <span>Postuler</span>
                      <ExternalLink className="w-3.5 h-3.5" />
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