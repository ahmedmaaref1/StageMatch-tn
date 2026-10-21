import React, { useState } from 'react';
import { 
  Kanban as KanbanIcon, 
  Building2, 
  MapPin, 
  Calendar, 
  ArrowRight, 
  ArrowLeft, 
  Trash2, 
  ExternalLink, 
  Edit3, 
  Save, 
  X, 
  Plus, 
  CheckCircle2, 
  Clock, 
  Sparkles,
  MessageSquare,
  Search,
  Filter
} from 'lucide-react';

const COLUMNS = [
  {
    id: 'saved',
    title: 'À postuler',
    subtitle: 'Wishlist & Sujets repérés',
    badgeClass: 'bg-slate-100 text-slate-700 border-slate-200',
    headerBorder: 'border-slate-300',
    dotColor: 'bg-slate-400',
    headerBg: 'bg-slate-100/50',
  },
  {
    id: 'applied',
    title: 'Candidature envoyée',
    subtitle: 'CV et lettre transmis',
    badgeClass: 'bg-blue-50 text-blue-700 border-blue-200',
    headerBorder: 'border-blue-400',
    dotColor: 'bg-blue-500',
    headerBg: 'bg-blue-50/40',
  },
  {
    id: 'interview',
    title: 'Entretien Technique / RH',
    subtitle: 'Entretiens planifiés',
    badgeClass: 'bg-purple-50 text-purple-700 border-purple-200',
    headerBorder: 'border-purple-400',
    dotColor: 'bg-purple-500',
    headerBg: 'bg-purple-50/40',
  },
  {
    id: 'offer',
    title: 'Offre reçue & Validée',
    subtitle: 'Convention PFE prête 🎉',
    badgeClass: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    headerBorder: 'border-emerald-400',
    dotColor: 'bg-emerald-500',
    headerBg: 'bg-emerald-50/40',
  },
];

export default function Kanban({ 
  applications = [], 
  onUpdateApplication, 
  onRemoveApplication, 
  onAddApplication,
  setActiveTab 
}) {
  const [editingNoteId, setEditingNoteId] = useState(null);
  const [tempNote, setTempNote] = useState('');
  const [searchKanban, setSearchKanban] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [newApp, setNewApp] = useState({
    title: '',
    company: '',
    city: 'Tunis',
    domain: 'IA, Data & Machine Learning',
    source_url: '',
    notes: '',
    status: 'saved',
  });

  // Filter applications by search term
  const filteredApps = applications.filter(app => {
    if (!searchKanban.trim()) return true;
    const q = searchKanban.toLowerCase();
    return (
      app.company?.toLowerCase().includes(q) ||
      app.title?.toLowerCase().includes(q) ||
      app.domain?.toLowerCase().includes(q) ||
      app.notes?.toLowerCase().includes(q)
    );
  });

  const getColItems = (colId) => filteredApps.filter(app => app.status === colId);

  const moveStatus = (appId, direction) => {
    const statusOrder = ['saved', 'applied', 'interview', 'offer'];
    const currentApp = applications.find(a => a.id === appId);
    if (!currentApp) return;

    const currentIndex = statusOrder.indexOf(currentApp.status);
    const newIndex = direction === 'next' ? currentIndex + 1 : currentIndex - 1;

    if (newIndex >= 0 && newIndex < statusOrder.length) {
      onUpdateApplication(appId, { 
        status: statusOrder[newIndex],
        last_updated: new Date().toISOString()
      });
    }
  };

  const handleStartEditNote = (app) => {
    setEditingNoteId(app.id);
    setTempNote(app.notes || '');
  };

  const handleSaveNote = (appId) => {
    onUpdateApplication(appId, { notes: tempNote });
    setEditingNoteId(null);
  };

  const handleCreateManualApp = (e) => {
    e.preventDefault();
    if (!newApp.title || !newApp.company) return;

    const created = {
      ...newApp,
      id: 'manual_' + Date.now(),
      date_added: new Date().toISOString().split('T')[0],
      source_site: 'Candidature Spontanée',
    };

    onAddApplication(created);
    setShowAddModal(false);
    setNewApp({
      title: '',
      company: '',
      city: 'Tunis',
      domain: 'IA, Data & Machine Learning',
      source_url: '',
      notes: '',
      status: 'saved',
    });
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 pb-2 border-b border-slate-200">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-xs font-semibold mb-1">
            <KanbanIcon className="w-3.5 h-3.5 text-blue-600" />
            <span>PFE Career CRM & Pipeline</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Suivi de vos Candidatures PFE
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
            Organisez vos démarches, planifiez vos entretiens et notez les retours des recruteurs en Tunisie.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setShowAddModal(true)}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-2xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold shadow-xs transition-colors"
          >
            <Plus className="w-4 h-4" />
            <span>Ajouter une candidature</span>
          </button>
        </div>
      </div>

      {/* Filter and Overview Bar */}
      <div className="bg-white rounded-3xl p-4 sm:p-5 border border-slate-200/90 shadow-xs flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        
        {/* KPI Chips */}
        <div className="flex flex-wrap items-center gap-2">
          {COLUMNS.map((col) => {
            const count = applications.filter(a => a.status === col.id).length;
            return (
              <div 
                key={col.id} 
                className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-50 border border-slate-200/80 text-xs"
              >
                <span className={`w-2.5 h-2.5 rounded-full ${col.dotColor}`} />
                <span className="font-semibold text-slate-700">{col.title} :</span>
                <span className="font-black text-slate-900">{count}</span>
              </div>
            );
          })}
        </div>

        {/* Quick Search in Kanban */}
        {applications.length > 0 && (
          <div className="relative w-full sm:w-64">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchKanban}
              onChange={(e) => setSearchKanban(e.target.value)}
              placeholder="Filtrer mes candidatures..."
              className="w-full pl-9 pr-7 py-1.5 rounded-xl border border-slate-200 text-xs focus:outline-hidden focus:ring-2 focus:ring-blue-500 bg-slate-50 focus:bg-white"
            />
            {searchKanban && (
              <button
                onClick={() => setSearchKanban('')}
                className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
              >
                <X className="w-3 h-3" />
              </button>
            )}
          </div>
        )}
      </div>

      {/* Empty State Banner if 0 applications */}
      {applications.length === 0 ? (
        <div className="bg-white rounded-3xl p-12 text-center border border-slate-200/90 shadow-xs max-w-xl mx-auto space-y-5">
          <div className="w-16 h-16 rounded-3xl bg-blue-50 text-blue-600 flex items-center justify-center mx-auto shadow-xs border border-blue-100">
            <KanbanIcon className="w-8 h-8" />
          </div>
          <div className="space-y-2">
            <h2 className="text-xl font-bold text-slate-900">Aucune candidature enregistrée pour le moment</h2>
            <p className="text-xs text-slate-600 leading-relaxed max-w-md mx-auto">
              Parcourez le catalogue des offres ou vos recommandations par IA, puis cliquez sur <strong>"Suivre"</strong> pour organiser votre recrutement ici.
            </p>
          </div>
          <div className="pt-2 flex flex-col sm:flex-row gap-3 justify-center">
            <button
              onClick={() => setActiveTab('recommendations')}
              className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-2xl bg-blue-600 text-white text-xs font-bold hover:bg-blue-700 transition-colors shadow-xs"
            >
              <Sparkles className="w-4 h-4" />
              <span>Voir mes recommandations IA</span>
            </button>
            <button
              onClick={() => setActiveTab('offers')}
              className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-2xl bg-slate-100 text-slate-700 text-xs font-bold hover:bg-slate-200 transition-colors"
            >
              <span>Explorer les 58 offres</span>
            </button>
          </div>
        </div>
      ) : (
        /* The 4 Kanban Columns */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 items-start">
          {COLUMNS.map((col, colIdx) => {
            const items = getColItems(col.id);
            return (
              <div 
                key={col.id} 
                className="bg-slate-100/60 rounded-3xl p-4 border border-slate-200/90 flex flex-col min-h-[520px]"
              >
                {/* Column Header */}
                <div className={`pb-3 mb-3 border-b-2 ${col.headerBorder} flex items-center justify-between`}>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className={`w-2.5 h-2.5 rounded-full ${col.dotColor}`}></span>
                      <h3 className="font-bold text-xs sm:text-sm text-slate-900">{col.title}</h3>
                    </div>
                    <span className="text-[10px] text-slate-400 block mt-0.5">{col.subtitle}</span>
                  </div>
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${col.badgeClass}`}>
                    {items.length}
                  </span>
                </div>

                {/* Column Cards */}
                <div className="space-y-3 flex-1 overflow-y-auto">
                  {items.length === 0 ? (
                    <div className="py-10 px-4 text-center border-2 border-dashed border-slate-200/90 rounded-2xl text-xs text-slate-400">
                      Aucun sujet dans cette étape
                    </div>
                  ) : (
                    items.map((app) => (
                      <div 
                        key={app.id} 
                        className="bg-white rounded-2xl p-4 border border-slate-200/90 shadow-2xs hover:shadow-md transition-all space-y-3 relative group"
                      >
                        {/* Company & Delete Action */}
                        <div className="flex items-start justify-between gap-2">
                          <div className="flex items-center gap-2 text-xs font-bold text-slate-800">
                            <div className="w-5 h-5 rounded-md bg-blue-50 text-blue-600 font-extrabold text-[10px] flex items-center justify-center shrink-0 border border-blue-100">
                              {app.company ? app.company[0].toUpperCase() : 'E'}
                            </div>
                            <span className="line-clamp-1">{app.company}</span>
                          </div>
                          <button
                            onClick={() => onRemoveApplication(app.id)}
                            title="Supprimer du suivi"
                            className="text-slate-300 hover:text-red-500 transition-colors p-1"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </div>

                        {/* Title */}
                        <h4 className="text-xs font-bold text-slate-900 leading-snug line-clamp-2">
                          {app.title}
                        </h4>

                        {/* Domain & City Badges */}
                        <div className="flex flex-wrap items-center gap-1.5 text-[10px]">
                          <span className="px-2 py-0.5 rounded-md bg-slate-100 text-slate-600 font-medium">
                            {app.city || 'Tunis'}
                          </span>
                          {app.domain && (
                            <span className="px-2 py-0.5 rounded-md bg-blue-50 text-blue-700 font-medium line-clamp-1">
                              {app.domain}
                            </span>
                          )}
                        </div>

                        {/* Personal Notes Section */}
                        <div className="pt-2 border-t border-slate-100 text-xs">
                          {editingNoteId === app.id ? (
                            <div className="space-y-2">
                              <textarea
                                value={tempNote}
                                onChange={(e) => setTempNote(e.target.value)}
                                placeholder="Note (ex: Entretien prévu avec M. X, questions préparées...)"
                                rows={2}
                                className="w-full text-xs p-2 rounded-xl border border-blue-400 focus:outline-hidden focus:ring-1 focus:ring-blue-500"
                              />
                              <div className="flex justify-end gap-1.5">
                                <button
                                  onClick={() => setEditingNoteId(null)}
                                  className="p-1 text-slate-400 hover:text-slate-600 text-[10px]"
                                >
                                  <X className="w-3.5 h-3.5" />
                                </button>
                                <button
                                  onClick={() => handleSaveNote(app.id)}
                                  className="inline-flex items-center gap-1 px-2.5 py-1 bg-blue-600 text-white rounded-lg text-[10px] font-bold"
                                >
                                  <Save className="w-3 h-3" />
                                  <span>Sauvegarder</span>
                                </button>
                              </div>
                            </div>
                          ) : (
                            <div 
                              onClick={() => handleStartEditNote(app)}
                              className="cursor-pointer group/note p-1.5 rounded-xl hover:bg-slate-50 transition-colors flex items-start justify-between gap-1"
                            >
                              <div className="flex items-start gap-1.5 text-slate-500 text-[11px] leading-relaxed">
                                <MessageSquare className="w-3.5 h-3.5 shrink-0 text-slate-400 mt-0.5" />
                                <span className={app.notes ? 'text-slate-700 font-medium' : 'italic text-slate-400'}>
                                  {app.notes || 'Ajouter une note de suivi...'}
                                </span>
                              </div>
                              <Edit3 className="w-3 h-3 text-slate-300 opacity-0 group-hover/note:opacity-100 shrink-0" />
                            </div>
                          )}
                        </div>

                        {/* Card Footer: Movement Controls & External Link */}
                        <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs">
                          {colIdx > 0 ? (
                            <button
                              onClick={() => moveStatus(app.id, 'prev')}
                              title="Déplacer vers l'étape précédente"
                              className="p-1 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors"
                            >
                              <ArrowLeft className="w-3.5 h-3.5" />
                            </button>
                          ) : <div className="w-4" />}

                          {app.source_url && (
                            <a
                              href={app.source_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-1 text-[11px] text-blue-600 hover:text-blue-800 font-bold"
                            >
                              <span>Offre</span>
                              <ExternalLink className="w-3 h-3" />
                            </a>
                          )}

                          {colIdx < COLUMNS.length - 1 ? (
                            <button
                              onClick={() => moveStatus(app.id, 'next')}
                              title="Avancer vers l'étape suivante"
                              className="p-1 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-lg transition-colors flex items-center gap-1 font-bold text-[10px]"
                            >
                              <span>Avancer</span>
                              <ArrowRight className="w-3.5 h-3.5" />
                            </button>
                          ) : (
                            <span className="text-emerald-600 flex items-center gap-0.5 text-[11px] font-extrabold">
                              <CheckCircle2 className="w-3.5 h-3.5" />
                              <span>Validé</span>
                            </span>
                          )}
                        </div>

                      </div>
                    ))
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Manual Application Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl p-6 sm:p-7 max-w-lg w-full shadow-2xl space-y-5 animate-fade-in">
            <div className="flex items-center justify-between pb-3 border-b border-slate-200">
              <div className="flex items-center gap-2">
                <KanbanIcon className="w-5 h-5 text-blue-600" />
                <h3 className="text-lg font-bold text-slate-900">Ajouter une candidature manuelle</h3>
              </div>
              <button 
                onClick={() => setShowAddModal(false)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreateManualApp} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Intitulé du Sujet PFE *
                </label>
                <input
                  type="text"
                  required
                  placeholder="ex: Conception d'un pipeline MLOps avec Kubeflow"
                  value={newApp.title}
                  onChange={(e) => setNewApp({ ...newApp, title: e.target.value })}
                  className="w-full text-xs p-2.5 rounded-xl border border-slate-300 focus:outline-hidden focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Entreprise *
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="ex: Vermeg, Telnet, Satoripop"
                    value={newApp.company}
                    onChange={(e) => setNewApp({ ...newApp, company: e.target.value })}
                    className="w-full text-xs p-2.5 rounded-xl border border-slate-300 focus:outline-hidden focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Gouvernorat / Ville
                  </label>
                  <input
                    type="text"
                    placeholder="ex: Tunis, Lac 2, Sousse"
                    value={newApp.city}
                    onChange={(e) => setNewApp({ ...newApp, city: e.target.value })}
                    className="w-full text-xs p-2.5 rounded-xl border border-slate-300 focus:outline-hidden focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Filière Technologique
                  </label>
                  <select
                    value={newApp.domain}
                    onChange={(e) => setNewApp({ ...newApp, domain: e.target.value })}
                    className="w-full text-xs p-2.5 rounded-xl border border-slate-300 focus:outline-hidden focus:ring-2 focus:ring-blue-500 bg-white"
                  >
                    <option>IA, Data & Machine Learning</option>
                    <option>Web & Fullstack</option>
                    <option>Backend & Microservices</option>
                    <option>DevOps & Cloud</option>
                    <option>Mobile Development</option>
                    <option>Cybersécurité & Réseaux</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Étape initiale
                  </label>
                  <select
                    value={newApp.status}
                    onChange={(e) => setNewApp({ ...newApp, status: e.target.value })}
                    className="w-full text-xs p-2.5 rounded-xl border border-slate-300 focus:outline-hidden focus:ring-2 focus:ring-blue-500 bg-white"
                  >
                    <option value="saved">À postuler (Sauvegardé)</option>
                    <option value="applied">Candidature envoyée</option>
                    <option value="interview">Entretien planifié</option>
                    <option value="offer">Offre reçue</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Lien de l'offre ou contact RH (optionnel)
                </label>
                <input
                  type="url"
                  placeholder="https://..."
                  value={newApp.source_url}
                  onChange={(e) => setNewApp({ ...newApp, source_url: e.target.value })}
                  className="w-full text-xs p-2.5 rounded-xl border border-slate-300 focus:outline-hidden focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Notes personnelles
                </label>
                <textarea
                  rows={2}
                  placeholder="ex: Recommandé par mon enseignant encadrant..."
                  value={newApp.notes}
                  onChange={(e) => setNewApp({ ...newApp, notes: e.target.value })}
                  className="w-full text-xs p-2.5 rounded-xl border border-slate-300 focus:outline-hidden focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div className="pt-3 flex justify-end gap-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 text-xs font-bold text-slate-600 hover:bg-slate-100 rounded-xl transition-colors"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 text-xs font-bold bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-xs transition-colors"
                >
                  Ajouter au tableau
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
