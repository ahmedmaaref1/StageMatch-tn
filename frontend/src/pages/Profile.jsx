import React, { useState } from 'react';
import { 
  User, 
  Sparkles, 
  GraduationCap, 
  MapPin, 
  Mail, 
  BookOpen, 
  Plus, 
  X, 
  Check, 
  UploadCloud, 
  Loader2,
  CheckCircle2,
  AlertCircle,
  Award,
  Zap
} from 'lucide-react';
import { createOrUpdateStudent, parseStudentCV } from '../api';

const TUNISIAN_UNIVERSITIES = [
  // Grandes Écoles d'Ingénieurs
  "INSAT (Tunis)",
  "ENSI (Manouba)",
  "SUP'COM (El Ghazala)",
  "ENIT (Tunis)",
  "ENISo (Sousse)",
  "ENIS (Sfax)",
  "ENIM (Monastir)",
  "ENSIT (Tunis)",
  "EPT (La Marsa)",
  "ENIB (Bizerte)",
  "ENICarthage",
  
  // Instituts Spécialisés d'Informatique
  "ISI (Ariana / El Manar)",
  "ISITCom (Hammam Sousse)",
  "ISIMM (Monastir)",
  "ISIMS (Sfax)",
  "ISIMG (Gabès)",
  "ISAMM (Manouba)",
  "ISIGK (Kairouan)",
  "ISIK (Le Kef)",
  "ISLAIB (Béja)",
  "ISG Tunis (Business Analytics)",
  "ESSTHS (Hammam Sousse)",
  
  // Réseau ISSAT
  "ISSAT Sousse",
  "ISSAT Mahdia",
  "ISSAT Kairouan",
  "ISSAT Gafsa",
  "ISSAT Kasserine",
  "ISSAT Mateur",

  // Facultés des Sciences
  "FST (El Manar - Informatique)",
  "FSS (Sfax - Informatique)",
  "FSM (Monastir - Informatique)",
  "FSB (Bizerte - Informatique)",
  
  // Réseau ISET
  "ISET'Com (El Ghazala)",
  "ISET Rades",
  "ISET Sousse",
  "ISET Sfax",
  "ISET Nabeul",
  "ISET Bizerte",
  "ISET Kélibia",
  "ISET Mahdia",
  "ISET Djerba",
  "ISET Gabès",
  
  // Écoles Privées d'Ingénieurs
  "ESPRIT",
  "MedTech (SMU - Lac 2)",
  "TEK-UP (El Ghazala)",
  "SESAME (El Ghazala)",
  "EPI (Sousse)",
  "IIT (Sfax)",
  "Polytechnique Intl",
  
  "Autre établissement IT en Tunisie"
];

const DOMAINS = [
  "Web & Fullstack",
  "Backend & Microservices",
  "IA, Data & Machine Learning",
  "DevOps & Cloud",
  "Mobile Development",
  "Cybersécurité & Réseaux"
];

const POPULAR_SKILLS = [
  "Docker",
  "Python",
  "FastAPI",
  "React",
  "PostgreSQL",
  "Git",
  "TypeScript",
  "Spring Boot",
  "Kubernetes",
  "PyTorch",
  "Next.js",
  "Flutter",
  "CI/CD",
  "Linux",
  "Node.js",
  "MongoDB",
  "Kafka",
  "Angular"
];

export default function Profile({ student, setStudent, setActiveTab, showToast }) {
  const [formData, setFormData] = useState({
    full_name: student?.full_name || '',
    email: student?.email || '',
    university: student?.university || 'INSAT (Tunis)',
    degree_level: student?.degree_level || 'Cycle Ingénieur 3',
    domain: student?.domain || 'IA, Data & Machine Learning',
    preferred_city: student?.preferred_city || 'Tunis',
    bio: student?.bio || '',
    skills: student?.skills || ['Python', 'FastAPI', 'React', 'Docker'],
  });

  const [skillInput, setSkillInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);
  const [parsingCV, setParsingCV] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);

  // Calculate profile completion score
  const calculateCompletion = () => {
    let score = 0;
    if (formData.full_name.trim()) score += 15;
    if (formData.email.trim()) score += 15;
    if (formData.university) score += 15;
    if (formData.degree_level) score += 15;
    if (formData.domain) score += 15;
    if (formData.preferred_city.trim()) score += 10;
    if (formData.skills.length >= 3) score += 15;
    return Math.min(score, 100);
  };

  const completionPct = calculateCompletion();

  const handleFileUpload = async (file) => {
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setError("Veuillez sélectionner un fichier PDF valide.");
      return;
    }

    try {
      setParsingCV(true);
      setError(null);
      const parsed = await parseStudentCV(file);

      // Match university with one in our Tunisian dropdown list
      let matchedUni = formData.university;
      if (parsed.university) {
        const found = TUNISIAN_UNIVERSITIES.find(u => 
          u.toLowerCase().includes(parsed.university.toLowerCase()) || 
          parsed.university.toLowerCase().includes(u.toLowerCase())
        );
        if (found) matchedUni = found;
      }

      // Merge newly extracted skills with existing skills without duplicates
      const mergedSkills = Array.from(new Set([...formData.skills, ...(parsed.skills || [])]));

      setFormData(prev => ({
        ...prev,
        full_name: parsed.full_name || prev.full_name,
        email: parsed.email || prev.email,
        university: matchedUni,
        domain: parsed.domain || prev.domain,
        skills: mergedSkills,
      }));

      const msg = `🎉 CV analysé avec succès ! ${parsed.skills?.length || 0} compétences détectées.`;
      setSuccess(msg);
      if (showToast) showToast(msg, 'success');
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Erreur lors de l'analyse du CV.");
    } finally {
      setParsingCV(false);
    }
  };

  const handleAddSkill = (e) => {
    e.preventDefault();
    if (skillInput.trim()) {
      const newSkills = skillInput
        .split(',')
        .map(s => s.trim())
        .filter(s => s.length > 0 && !formData.skills.includes(s));

      if (newSkills.length > 0) {
        setFormData({
          ...formData,
          skills: [...formData.skills, ...newSkills]
        });
      }
      setSkillInput('');
    }
  };

  const handleAddPopularSkill = (skill) => {
    if (!formData.skills.includes(skill)) {
      setFormData(prev => ({
        ...prev,
        skills: [...prev.skills, skill]
      }));
    }
  };

  const handleRemoveSkill = (skillToRemove) => {
    setFormData({
      ...formData,
      skills: formData.skills.filter(s => s !== skillToRemove)
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const savedStudent = await createOrUpdateStudent(formData);
      setStudent(savedStudent);
      localStorage.setItem('stagematch_student', JSON.stringify(savedStudent));
      setSuccess(true);
      if (showToast) showToast("Profil enregistré ! Calcul des recommandations...", 'success');
      
      // Auto-switch to recommendations after 1.2 seconds
      setTimeout(() => {
        setActiveTab('recommendations');
      }, 1200);

    } catch (err) {
      console.error(err);
      setError("Erreur lors de l'enregistrement. Vérifiez vos informations.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8 space-y-6">
      
      {/* Header with Completion Card */}
      <div className="bg-white border border-slate-200/90 rounded-3xl p-6 shadow-xs flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-xs font-semibold mb-1">
            <User className="w-3.5 h-3.5" />
            <span>Profil Étudiant & CV</span>
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
            Configuration de votre Profil
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Ces critères alimentent directement les calculs sémantiques de l'IA pour vous trouver les meilleurs stages.
          </p>
        </div>

        {/* Completion Progress Bar */}
        <div className="w-full sm:w-56 p-3 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2 shrink-0">
          <div className="flex justify-between items-center text-xs">
            <span className="font-bold text-slate-700">Complétion</span>
            <span className="font-extrabold text-blue-600">{completionPct}%</span>
          </div>
          <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden">
            <div 
              className={`h-full rounded-full transition-all duration-500 ${
                completionPct === 100 
                  ? 'bg-emerald-500' 
                  : completionPct >= 70 
                    ? 'bg-blue-600' 
                    : 'bg-amber-500'
              }`}
              style={{ width: `${completionPct}%` }}
            />
          </div>
          <span className="text-[10px] text-slate-400 block text-right font-medium">
            {completionPct === 100 ? 'Profil optimal pour le matching !' : 'Ajoutez vos compétences clés'}
          </span>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-2xl bg-red-50 border border-red-200 text-red-700 text-xs font-medium flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {success && (
        <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-medium flex items-center gap-2 animate-fade-in">
          <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-600" />
          <span>{typeof success === 'string' ? success : 'Profil enregistré avec succès ! Redirection vers vos recommandations...'}</span>
        </div>
      )}

      {/* Main Form Box */}
      <div className="bg-white border border-slate-200/90 rounded-3xl p-6 sm:p-8 shadow-xs space-y-6">
        
        {/* 📄 CV Upload Dropzone */}
        <div 
          onDragOver={(e) => { e.preventDefault(); setIsDragOver(true); }}
          onDragLeave={() => setIsDragOver(false)}
          onDrop={(e) => {
            e.preventDefault();
            setIsDragOver(false);
            const file = e.dataTransfer.files?.[0];
            if (file) handleFileUpload(file);
          }}
          className={`p-6 border-2 border-dashed rounded-3xl transition-all text-center relative cursor-pointer ${
            isDragOver 
              ? 'border-blue-500 bg-blue-50/80 scale-[1.01]' 
              : 'border-indigo-200 hover:border-indigo-400 bg-indigo-50/30 hover:bg-indigo-50/60'
          }`}
        >
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => handleFileUpload(e.target.files?.[0])}
            disabled={parsingCV}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed"
          />
          <div className="flex flex-col items-center justify-center space-y-2 pointer-events-none">
            {parsingCV ? (
              <>
                <Loader2 className="w-9 h-9 text-indigo-600 animate-spin" />
                <p className="text-sm font-extrabold text-indigo-900">Analyse IA de votre CV en cours...</p>
                <p className="text-xs text-indigo-600">Extraction des compétences techniques et détection de l'université...</p>
              </>
            ) : (
              <>
                <div className="w-12 h-12 rounded-2xl bg-indigo-600/10 text-indigo-600 flex items-center justify-center shadow-2xs">
                  <UploadCloud className="w-6 h-6" />
                </div>
                <div>
                  <p className="text-sm font-bold text-slate-800">
                    📄 Remplissage automatique par CV (PDF)
                  </p>
                  <p className="text-xs text-slate-500 mt-0.5">
                    Glissez-déposez votre CV ici ou <span className="text-indigo-600 font-bold underline">cliquez pour parcourir</span>
                  </p>
                </div>
                <span className="text-[10px] font-semibold text-slate-400 bg-white px-3 py-0.5 rounded-full border border-slate-200">
                  Format .PDF (INSAT, ESPRIT, ENIT, ISI...)
                </span>
              </>
            )}
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Nom Complet *
              </label>
              <input
                type="text"
                required
                value={formData.full_name}
                onChange={e => setFormData({ ...formData, full_name: e.target.value })}
                placeholder="ex: Ahmed Ben Salem"
                className="w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:outline-hidden focus:ring-2 focus:ring-blue-500 text-xs sm:text-sm bg-slate-50/50 focus:bg-white"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Email *
              </label>
              <input
                type="email"
                required
                value={formData.email}
                onChange={e => setFormData({ ...formData, email: e.target.value })}
                placeholder="ahmed@gmail.com"
                className="w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:outline-hidden focus:ring-2 focus:ring-blue-500 text-xs sm:text-sm bg-slate-50/50 focus:bg-white"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Université / Faculté *
              </label>
              <select
                value={formData.university}
                onChange={e => setFormData({ ...formData, university: e.target.value })}
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 focus:outline-hidden focus:ring-2 focus:ring-blue-500 text-xs sm:text-sm bg-white"
              >
                {TUNISIAN_UNIVERSITIES.map(u => (
                  <option key={u} value={u}>{u}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Niveau d'études *
              </label>
              <select
                value={formData.degree_level}
                onChange={e => setFormData({ ...formData, degree_level: e.target.value })}
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 focus:outline-hidden focus:ring-2 focus:ring-blue-500 text-xs sm:text-sm bg-white"
              >
                <option value="Cycle Ingénieur 3">Cycle Ingénieur (PFE)</option>
                <option value="Master 2">Master 2 (PFE)</option>
                <option value="Licence 3">Licence 3 (PFE)</option>
                <option value="Licence 2">Licence 2 (Stage été)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Ville Préférée
              </label>
              <input
                type="text"
                value={formData.preferred_city}
                onChange={e => setFormData({ ...formData, preferred_city: e.target.value })}
                placeholder="ex: Tunis, Lac 2, Sousse..."
                className="w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:outline-hidden focus:ring-2 focus:ring-blue-500 text-xs sm:text-sm bg-slate-50/50 focus:bg-white"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Filière Principale *
            </label>
            <select
              value={formData.domain}
              onChange={e => setFormData({ ...formData, domain: e.target.value })}
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 focus:outline-hidden focus:ring-2 focus:ring-blue-500 text-xs sm:text-sm bg-white"
            >
              {DOMAINS.map(d => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
          </div>

          {/* Skills Tag Input */}
          <div className="space-y-3 pt-2 border-t border-slate-100">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                Compétences Techniques & Frameworks ({formData.skills.length})
              </label>
              <p className="text-xs text-slate-500 mb-2">
                Tapez une compétence et appuyez sur Entrée, ou cliquez sur les suggestions ci-dessous.
              </p>
            </div>

            {/* Input field */}
            <div className="flex gap-2">
              <input
                type="text"
                value={skillInput}
                onChange={e => setSkillInput(e.target.value)}
                onKeyDown={e => { if (e.key === 'Enter') handleAddSkill(e); }}
                placeholder="ex: Docker, FastAPI, PyTorch (séparés par virgule)"
                className="flex-1 px-4 py-2.5 rounded-xl border border-slate-200 focus:outline-hidden focus:ring-2 focus:ring-blue-500 text-xs sm:text-sm"
              />
              <button
                type="button"
                onClick={handleAddSkill}
                className="px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold rounded-xl text-xs flex items-center gap-1 transition-colors"
              >
                <Plus className="w-4 h-4" />
                <span>Ajouter</span>
              </button>
            </div>

            {/* Popular Skills Quick-Add Row */}
            <div className="space-y-1.5 pt-1">
              <span className="text-[11px] font-semibold text-slate-400">Suggestions populaires en Tunisie :</span>
              <div className="flex flex-wrap gap-1.5">
                {POPULAR_SKILLS.filter(s => !formData.skills.includes(s)).slice(0, 10).map(skill => (
                  <button
                    key={skill}
                    type="button"
                    onClick={() => handleAddPopularSkill(skill)}
                    className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-slate-50 hover:bg-blue-50 hover:text-blue-700 border border-slate-200/80 text-[11px] font-semibold text-slate-600 transition-colors"
                  >
                    <Plus className="w-3 h-3 text-blue-500" />
                    <span>{skill}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Currently Selected Skills Badges */}
            <div className="flex flex-wrap gap-1.5 pt-2">
              {formData.skills.map(skill => (
                <span
                  key={skill}
                  className="inline-flex items-center gap-1.5 px-3 py-1 rounded-xl bg-blue-50 text-blue-800 border border-blue-200/90 text-xs font-bold animate-fade-in"
                >
                  <span>{skill}</span>
                  <button
                    type="button"
                    onClick={() => handleRemoveSkill(skill)}
                    className="hover:text-red-600 p-0.5 rounded-full"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                </span>
              ))}
            </div>
          </div>

          {/* Submit Button */}
          <div className="pt-4 border-t border-slate-100 flex justify-end">
            <button
              type="submit"
              disabled={loading}
              className="flex items-center justify-center gap-2 px-7 py-3 rounded-2xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold text-sm shadow-md shadow-blue-500/25 transition-all hover:scale-[1.01] disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Enregistrement...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>Enregistrer et Calculer les Matchs IA</span>
                </>
              )}
            </button>
          </div>

        </form>

      </div>

    </div>
  );
}