import { useNavigate } from 'react-router-dom';
import { AlertTriangle, X } from 'lucide-react';

export default function AlertModal({ subject, onDismiss, onViewProfile, onLogOffence }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
      {/* Pulsing red border ring */}
      <div className="absolute inset-0 pointer-events-none border-4 border-accent-red animate-pulse" />

      <div className="relative bg-card-light dark:bg-[#1a0505] border-2 border-accent-red rounded-2xl max-w-md w-full shadow-2xl shadow-red-500/30 overflow-hidden">
        {/* Top urgency banner */}
        <div className="bg-accent-red px-5 py-3 flex items-center gap-3">
          <AlertTriangle className="w-6 h-6 text-white animate-pulse" />
          <div>
            <div className="text-white font-bold tracking-widest text-sm uppercase">⚠ WANTED INDIVIDUAL DETECTED</div>
            <div className="text-red-100 text-xs font-mono">IMMEDIATE ACTION REQUIRED</div>
          </div>
        </div>

        {/* Body */}
        <div className="p-5 space-y-4">
          <div className="flex items-center gap-4">
            <img
              src={subject.mugshotUrl}
              alt={subject.name}
              className="w-20 h-20 rounded-xl object-cover border-2 border-accent-red"
            />
            <div>
              <div className="text-xs font-mono text-gray-400">SUBJECT ID</div>
              <div className="text-xs font-mono text-accent-red">{subject.id}</div>
              <div className="text-xl font-bold text-text-primary-light dark:text-text-primary mt-1">{subject.name}</div>
              <div className="text-xs text-gray-400">AKA: {subject.aliases?.join(', ')}</div>
            </div>
          </div>

          {/* Warrant details */}
          <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-3 space-y-1">
            <div className="text-xs font-mono text-accent-red font-bold uppercase tracking-wider">Active Warrant</div>
            <div className="text-sm text-text-primary-light dark:text-text-primary">{subject.warrantDetails?.reason}</div>
            <div className="text-xs text-gray-400 font-mono">Issued: {subject.warrantDetails?.date} · {subject.warrantDetails?.issuedBy}</div>
          </div>

          {/* Confidence */}
          <div className="flex items-center justify-between text-xs font-mono bg-gray-100 dark:bg-white/5 rounded-lg px-3 py-2">
            <span className="text-gray-500">CONFIDENCE SCORE</span>
            <span className="text-accent-green font-bold text-base">{subject.confidence}%</span>
          </div>

          {/* Action buttons */}
          <div className="grid grid-cols-2 gap-3 pt-1">
            <button
              onClick={onViewProfile}
              className="btn-primary py-3 text-sm font-semibold tracking-wide"
            >
              View Profile
            </button>
            <button
              onClick={onLogOffence}
              className="btn-danger py-3 text-sm font-semibold tracking-wide"
            >
              Log Offence
            </button>
          </div>

          {/* Dismiss (hard to press - small, bottom text link) */}
          <button
            onClick={onDismiss}
            className="w-full text-center text-xs text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 py-1 transition-colors"
          >
            Dismiss (this action will be logged)
          </button>
        </div>
      </div>
    </div>
  );
}
