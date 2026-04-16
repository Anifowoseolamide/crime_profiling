import { useState, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import Webcam from 'react-webcam';
import { api } from '../services/api';
import { getCurrentLocation } from '../utils/location';
import AlertModal from '../components/ui/AlertModal';
import ConfidenceMeter from '../components/ui/ConfidenceMeter';
import StatusBadge from '../components/ui/StatusBadge';
import { Camera, RotateCcw, ZapOff, UserPlus, User, FileText } from 'lucide-react';

const STATES = { IDLE: 'IDLE', SCANNING: 'SCANNING', MATCH: 'MATCH', NO_MATCH: 'NO_MATCH' };

export default function FieldScan() {
  const navigate = useNavigate();
  const webcamRef = useRef(null);
  const [state, setState] = useState(STATES.IDLE);
  const [result, setResult] = useState(null);
  const [showWantedAlert, setShowWantedAlert] = useState(false);
  const [capturedImg, setCapturedImg] = useState(null);

  const capture = useCallback(async () => {
    const img = webcamRef.current?.getScreenshot();
    if (!img) return;
    setCapturedImg(img);
    setState(STATES.SCANNING);

    try {
      const coords = await getCurrentLocation();
      const data = await api.identifyFace(img, 'Field Scan', coords);
      setResult(data);
      if (data.match) {
        setState(STATES.MATCH);
        if (data.subject?.status === 'WANTED') {
          setTimeout(() => setShowWantedAlert(true), 400);
        }
      } else {
        setState(STATES.NO_MATCH);
      }
    } catch (err) {
      setState(STATES.IDLE);
    }
  }, [webcamRef]);

  const reset = () => {
    setState(STATES.IDLE);
    setResult(null);
    setCapturedImg(null);
    setShowWantedAlert(false);
  };

  return (
    <div className="max-w-lg mx-auto space-y-4 animate-fade-in">
      {/* Wanted alert modal */}
      {showWantedAlert && result?.subject && (
        <AlertModal
          subject={result.subject}
          onDismiss={() => setShowWantedAlert(false)}
          onViewProfile={() => navigate(`/subjects/${result.subject.id}`)}
          onLogOffence={() => navigate(`/offences/new?subject_id=${result.subject.id}`)}
        />
      )}

      {/* Header */}
      <div>
        <h1 className="text-lg font-bold text-text-primary-light dark:text-text-primary">Field Scan</h1>
        <p className="text-xs text-gray-500 dark:text-gray-400 font-mono">
          AI Facial Recognition · Real-time Identification
        </p>
      </div>

      {/* Camera / Result Card */}
      <div className="card-bg rounded-2xl overflow-hidden">
        {/* ── IDLE: show camera ── */}
        {state === STATES.IDLE && (
          <div className="scan-container">
            <Webcam
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              videoConstraints={{ facingMode: { ideal: 'environment' } }}
              className="w-full object-cover"
              style={{ maxHeight: '360px' }}
            />
            {/* Corner guides */}
            {['top-3 left-3', 'top-3 right-3', 'bottom-3 left-3', 'bottom-3 right-3'].map((pos, i) => (
              <div key={i} className={`absolute ${pos} w-6 h-6 border-accent-blue ${i < 2 ? 'border-t-2' : 'border-b-2'} ${i % 2 === 0 ? 'border-l-2' : 'border-r-2'}`} />
            ))}
            <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-4">
              <div className="text-xs font-mono text-white/60 text-center mb-3 tracking-widest uppercase">
                Center face in frame
              </div>
              <button
                id="capture-btn"
                onClick={capture}
                className="w-full bg-accent-blue hover:bg-blue-600 text-white py-3.5 rounded-xl font-bold text-sm flex items-center justify-center gap-2 transition-all shadow-lg shadow-accent-blue/30"
              >
                <Camera className="w-5 h-5" />
                Capture & Identify
              </button>
            </div>
          </div>
        )}

        {/* ── SCANNING: AI animation ── */}
        {state === STATES.SCANNING && (
          <div className="relative flex flex-col items-center justify-center py-12 px-6 gap-6">
            {capturedImg && (
              <div className="relative scan-container rounded-xl overflow-hidden">
                <img src={capturedImg} alt="Captured" className="w-40 h-40 object-cover rounded-xl grayscale" />
                <div className="scan-bar" />
                {/* Pulse ring */}
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <div className="w-32 h-32 rounded-full border-2 border-accent-blue animate-ping opacity-40" />
                </div>
              </div>
            )}
            <div className="text-center space-y-2">
              <div className="flex items-center justify-center gap-2">
                <span className="w-2 h-2 bg-accent-blue rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-2 h-2 bg-accent-blue rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-2 h-2 bg-accent-blue rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
              <div className="text-sm font-bold text-accent-blue font-mono tracking-widest animate-pulse uppercase">
                Scanning...
              </div>
              <div className="text-xs text-gray-500 dark:text-gray-400">
                Querying NCPRS database
              </div>
            </div>
          </div>
        )}

        {/* ── MATCH FOUND ── */}
        {state === STATES.MATCH && result?.subject && (
          <div className="p-5 space-y-4 animate-fade-in">
            <div className="flex items-center gap-2 text-accent-green">
              <div className="w-2 h-2 rounded-full bg-accent-green" />
              <span className="text-xs font-mono font-bold tracking-widest uppercase">Match Found</span>
            </div>
            <div className="flex items-center gap-4">
              <img
                src={result.subject.mugshotUrl}
                alt={result.subject.name}
                className="w-20 h-20 rounded-xl object-cover border-2 border-accent-green/40"
              />
              <div className="flex-1 min-w-0">
                <div className="text-xs font-mono text-gray-400">{result.subject.id}</div>
                <div className="text-lg font-bold text-text-primary-light dark:text-text-primary">{result.subject.name}</div>
                <div className="text-xs text-gray-500 mb-2">AKA: {result.subject.aliases?.join(', ')}</div>
                <StatusBadge status={result.subject.status} size="lg" />
              </div>
            </div>
            <ConfidenceMeter score={result.subject.confidence} />
            <div className="grid grid-cols-2 gap-3 pt-2">
              <button
                id="view-profile-btn"
                onClick={() => navigate(`/subjects/${result.subject.id}`)}
                className="btn-primary py-3 text-sm font-semibold flex items-center justify-center gap-2"
              >
                <User className="w-4 h-4" /> View Profile
              </button>
              <button
                onClick={() => navigate(`/offences/new?subject_id=${result.subject.id}`)}
                className="btn-danger py-3 text-sm font-semibold flex items-center justify-center gap-2"
              >
                <FileText className="w-4 h-4" /> Log Offence
              </button>
            </div>
            <button onClick={reset} className="w-full text-xs text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 py-1 flex items-center justify-center gap-1 transition-colors">
              <RotateCcw className="w-3 h-3" /> New Scan
            </button>
          </div>
        )}

        {/* ── NO MATCH ── */}
        {state === STATES.NO_MATCH && (
          <div className="p-8 flex flex-col items-center gap-4 text-center animate-fade-in">
            <div className="w-16 h-16 rounded-2xl bg-gray-100 dark:bg-white/5 flex items-center justify-center">
              <ZapOff className="w-8 h-8 text-gray-400" />
            </div>
            <div>
              <div className="text-sm font-bold text-text-primary-light dark:text-text-primary">No Existing Record Found</div>
              <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Subject is not in the NCPRS database.
              </div>
            </div>
            <div className="flex flex-col sm:flex-row gap-3 w-full pt-2">
              <button
                id="create-record-btn"
                onClick={() => navigate('/records/new')}
                className="flex-1 btn-primary py-3 text-sm font-semibold flex items-center justify-center gap-2"
              >
                <UserPlus className="w-4 h-4" /> Create New Record
              </button>
              <button
                onClick={reset}
                className="flex-1 py-3 text-sm font-semibold text-gray-500 dark:text-gray-400 border border-border-color-light dark:border-border-color rounded-md hover:bg-gray-100 dark:hover:bg-white/5 flex items-center justify-center gap-2 transition-colors"
              >
                <RotateCcw className="w-4 h-4" /> Try Again
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Instructions card (only when idle) */}
      {state === STATES.IDLE && (
        <div className="card-bg rounded-xl p-4 space-y-2">
          <div className="text-xs font-mono font-bold text-gray-400 uppercase tracking-widest">How to scan</div>
          {["Ensure subject face is well-lit and clearly visible", "Hold device steady for best results", "System will auto-query NCPRS database", "Wanted individuals trigger an immediate alert"].map((tip, i) => (
            <div key={i} className="flex items-start gap-2 text-xs text-gray-500 dark:text-gray-400">
              <span className="text-accent-blue font-mono mt-0.5">{i + 1}.</span>
              <span>{tip}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
