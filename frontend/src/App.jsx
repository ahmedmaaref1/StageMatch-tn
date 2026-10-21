import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Toast from './components/Toast';
import Home from './pages/Home';
import Profile from './pages/Profile';
import Offers from './pages/Offers';
import Recommendations from './pages/Recommendations';
import Analytics from './pages/Analytics';
import Kanban from './pages/Kanban';

export default function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [student, setStudent] = useState(null);
  const [toast, setToast] = useState(null);
  const [offerFilters, setOfferFilters] = useState({ search: '', domain: 'Tous les domaines' });

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
  };

  // Kanban applications state with localStorage persistence
  const [applications, setApplications] = useState(() => {
    try {
      const saved = localStorage.getItem('stagematch_kanban_apps');
      return saved ? JSON.parse(saved) : [];
    } catch (e) {
      return [];
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem('stagematch_kanban_apps', JSON.stringify(applications));
    } catch (e) {
      console.error('Failed to save applications to localStorage:', e);
    }
  }, [applications]);

  const handleToggleSave = (offer) => {
    setApplications(prev => {
      const exists = prev.find(a => a.id === offer.id);
      if (exists) {
        showToast(`Sujet retiré de votre suivi`, 'info');
        return prev.filter(a => a.id !== offer.id);
      } else {
        const newApp = {
          id: offer.id,
          title: offer.title,
          company: offer.company,
          city: offer.city || 'Tunis',
          domain: offer.domain,
          source_url: offer.source_url,
          source_site: offer.source_site,
          status: 'saved',
          notes: '',
          date_added: new Date().toISOString().split('T')[0],
        };
        showToast(`📌 "${offer.title.slice(0, 28)}..." ajouté au suivi !`, 'success');
        return [...prev, newApp];
      }
    });
  };

  const handleAddApplication = (newApp) => {
    setApplications(prev => [newApp, ...prev]);
    showToast(`Candidature pour "${newApp.company}" enregistrée`, 'success');
  };

  const handleUpdateApplication = (appId, updates) => {
    setApplications(prev => prev.map(a => a.id === appId ? { ...a, ...updates } : a));
    if (updates.status) {
      showToast(`Statut mis à jour`, 'info');
    }
  };

  const handleRemoveApplication = (appId) => {
    setApplications(prev => prev.filter(a => a.id !== appId));
    showToast(`Candidature supprimée`, 'info');
  };

  const isSaved = (offerId) => {
    return applications.some(a => a.id === offerId);
  };

  const navigateToOffers = ({ search = '', domain = 'Tous les domaines' } = {}) => {
    setOfferFilters({ search, domain });
    setActiveTab('offers');
  };

  // Load saved student from localStorage on initial page load
  useEffect(() => {
    const saved = localStorage.getItem('stagematch_student');
    if (saved) {
      try {
        setStudent(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to parse saved student:', e);
      }
    }
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 selection:bg-blue-600 selection:text-white">
      
      {/* Navigation Bar */}
      <Navbar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        applicationsCount={applications.length}
        student={student}
      />

      {/* Main Content Area */}
      <main className="grow">
        {activeTab === 'home' && (
          <Home 
            setActiveTab={setActiveTab}
            navigateToOffers={navigateToOffers}
            student={student}
          />
        )}

        {activeTab === 'profile' && (
          <Profile
            student={student}
            setStudent={setStudent}
            setActiveTab={setActiveTab}
            showToast={showToast}
          />
        )}

        {activeTab === 'offers' && (
          <Offers 
            isSaved={isSaved}
            onToggleSave={handleToggleSave}
            initialFilters={offerFilters}
            onResetFilters={() => setOfferFilters({ search: '', domain: 'Tous les domaines' })}
          />
        )}

        {activeTab === 'recommendations' && (
          <Recommendations
            student={student}
            setActiveTab={setActiveTab}
            isSaved={isSaved}
            onToggleSave={handleToggleSave}
          />
        )}

        {activeTab === 'kanban' && (
          <Kanban
            applications={applications}
            onUpdateApplication={handleUpdateApplication}
            onRemoveApplication={handleRemoveApplication}
            onAddApplication={handleAddApplication}
            setActiveTab={setActiveTab}
          />
        )}

        {activeTab === 'analytics' && (
          <Analytics
            setActiveTab={setActiveTab}
          />
        )}
      </main>

      {/* Floating Toast Notification */}
      <Toast toast={toast} onClose={() => setToast(null)} />

      {/* Footer */}
      <footer className="border-t border-slate-200/80 bg-white py-8 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4 text-xs text-slate-500">
            <div className="flex items-center gap-2">
              <span className="font-bold text-slate-800">StageMatch TN</span>
              <span>•</span>
              <span>Plateforme Universitaire PFE 2026</span>
            </div>
            <p className="text-center sm:text-right">
              Propulsé par FastAPI, PostgreSQL, React & Sentence-Transformers (NLP).
            </p>
          </div>
        </div>
      </footer>

    </div>
  );
}