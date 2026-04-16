import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Webcam from 'react-webcam';
import { ArrowLeft, ArrowRight, CheckCircle, Camera, Upload, User, Loader2 } from 'lucide-react';
import { api } from '../services/api';
import { getCurrentLocation } from '../utils/location';

const STEPS = ['Mugshot', 'Personal Details', 'Initial Offence'];

export default function CreateRecord() {
  const navigate = useNavigate();
  const webcamRef = useRef(null);
  const [step, setStep] = useState(0);
  const [useCamera, setUseCamera] = useState(true);
  const [mugshot, setMugshot] = useState(null);
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState(false);
  const [form, setForm] = useState({
    firstName: '', lastName: '', aliases: '', dob: '', gender: 'MALE',
    address: '', phone: '',
    offenceType: '', offenceDate: '', offenceLocation: '',
  });
  const [createdId, setCreatedId] = useState('');
  const [error, setError] = useState('');

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  const captureShot = () => {
    const img = webcamRef.current?.getScreenshot();
    if (img) setMugshot(img);
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    try {
      // 1. Create Subject
      const subjectData = {
        first_name: form.firstName,
        last_name: form.lastName,
        aliases: form.aliases ? form.aliases.split(',').map(s => s.trim()) : [],
        date_of_birth: form.dob || null,
        gender: form.gender.toUpperCase(),
        address: form.address,
        phone_numbers: form.phone ? [form.phone] : [],
      };
      
       const subject = await api.createSubject(subjectData);
      setCreatedId(subject.id);

      // Fetch coordinates once for the whole report
      const coords = await getCurrentLocation();

      // 2. Enrol Mugshot if available
      if (mugshot) {
        await api.enrolMugshot(subject.id, mugshot, coords);
      }

      // 3. Log Initial Offence if provided
      if (form.offenceType && form.offenceLocation) {
        await api.logOffence({
          subjectId: subject.id,
          type: form.offenceType,
          date: form.offenceDate,
          location: form.offenceLocation,
          latitude: coords?.lat,
          longitude: coords?.lng,
          notes: 'Initial offence logged during record creation.'
        });
      }

      setDone(true);
    } catch (err) {
      console.error('Failed to create record:', err);
      setError(err.message || 'Failed to create record. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (done) return (
    <div className="max-w-lg mx-auto animate-fade-in">
      <div className="card-bg rounded-2xl p-8 flex flex-col items-center gap-4 text-center">
        <div className="w-16 h-16 rounded-2xl bg-accent-green/15 flex items-center justify-center">
          <CheckCircle className="w-8 h-8 text-accent-green" />
        </div>
        <div>
          <div className="text-lg font-bold text-text-primary-light dark:text-text-primary">Record Created</div>
          <div className="text-xs text-gray-400 font-mono mt-1">LagosCP UUID</div>
          <div className="text-sm font-bold font-mono text-accent-blue mt-1 break-all">{createdId}</div>
        </div>
        <button onClick={() => navigate('/subjects')} className="w-full btn-primary py-3 text-sm">View All Subjects</button>
      </div>
    </div>
  );

  return (
    <div className="max-w-lg mx-auto space-y-4 animate-fade-in">
      <button onClick={() => navigate(-1)} className="flex items-center gap-1.5 text-xs text-gray-500 hover:text-text-primary-light dark:hover:text-text-primary transition-colors font-mono">
        <ArrowLeft className="w-3.5 h-3.5" /> Back
      </button>
      <div>
        <h1 className="text-lg font-bold text-text-primary-light dark:text-text-primary">Create New Record</h1>
        <p className="text-xs text-gray-500 font-mono">New subject entry — Step {step + 1} of {STEPS.length}</p>
      </div>

      {/* Step indicator */}
      <div className="flex items-center gap-1">
        {STEPS.map((s, i) => (
          <div key={s} className="flex items-center gap-1 flex-1">
            <div className={`w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-mono font-bold flex-shrink-0 transition-all ${
              i < step ? 'bg-accent-green text-white' : i === step ? 'bg-accent-blue text-white' : 'bg-gray-200 dark:bg-white/10 text-gray-400'
            }`}>
              {i < step ? '✓' : i + 1}
            </div>
            <div className={`text-[10px] font-mono hidden sm:block ${i === step ? 'text-accent-blue' : 'text-gray-400'}`}>
              {s}
            </div>
            {i < STEPS.length - 1 && <div className={`flex-1 h-px mx-1 ${i < step ? 'bg-accent-green' : 'bg-gray-200 dark:bg-white/10'}`} />}
          </div>
        ))}
      </div>

      <div className="card-bg rounded-2xl p-5">
        {/* Step 0: Mugshot */}
        {step === 0 && (
          <div className="space-y-4">
            <div className="flex gap-2 mb-3">
              {[['Camera', true], ['Upload', false]].map(([label, cam]) => (
                <button key={label} onClick={() => setUseCamera(cam)} className={`flex-1 py-2 text-xs font-mono rounded-lg transition-all ${useCamera === cam ? 'bg-accent-blue text-white' : 'bg-gray-100 dark:bg-white/5 text-gray-500'}`}>
                  {label}
                </button>
              ))}
            </div>
            {useCamera ? (
              <>
                {!mugshot ? (
                  <div className="rounded-xl overflow-hidden">
                    <Webcam ref={webcamRef} screenshotFormat="image/jpeg" className="w-full" style={{ maxHeight: '280px', objectFit: 'cover' }} />
                  </div>
                ) : (
                  <img src={mugshot} alt="Mugshot" className="w-full rounded-xl grayscale max-h-72 object-cover" />
                )}
                <button onClick={mugshot ? () => setMugshot(null) : captureShot} className={`w-full py-3 text-sm font-semibold rounded-xl flex items-center justify-center gap-2 ${mugshot ? 'border border-border-color-light dark:border-border-color text-gray-500' : 'btn-primary'}`}>
                  <Camera className="w-4 h-4" />{mugshot ? 'Retake' : 'Capture Mugshot'}
                </button>
              </>
            ) : (
              <label className="flex flex-col items-center gap-3 cursor-pointer border-2 border-dashed border-border-color-light dark:border-border-color rounded-xl px-4 py-10 hover:bg-gray-50 dark:hover:bg-white/5 transition-colors">
                <Upload className="w-8 h-8 text-gray-400" />
                <span className="text-sm text-gray-400">Click to upload mugshot photo</span>
                <input type="file" accept="image/*" className="hidden" onChange={e => {
                  const f = e.target.files[0];
                  if (f) { const r = new FileReader(); r.onload = ev => setMugshot(ev.target.result); r.readAsDataURL(f); }
                }} />
              </label>
            )}
          </div>
        )}

        {/* Step 1: Personal details */}
        {step === 1 && (
          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              {[['firstName', 'First Name'], ['lastName', 'Last Name']].map(([k, l]) => (
                <div key={k}>
                  <label className="block text-xs font-mono text-gray-500 uppercase tracking-wider mb-1">{l}</label>
                  <input type="text" value={form[k]} onChange={e => set(k, e.target.value)} className="input-field" />
                </div>
              ))}
            </div>
            {[['aliases', 'Aliases / Nicknames', 'text'], ['dob', 'Date of Birth', 'date'], ['address', 'Last Known Address', 'text'], ['phone', 'Phone Number', 'tel']].map(([k, l, t]) => (
              <div key={k}>
                <label className="block text-xs font-mono text-gray-500 uppercase tracking-wider mb-1">{l}</label>
                <input type={t} value={form[k]} onChange={e => set(k, e.target.value)} className="input-field" />
              </div>
            ))}
            <div>
              <label className="block text-xs font-mono text-gray-500 uppercase tracking-wider mb-1">Gender</label>
              <select value={form.gender} onChange={e => set('gender', e.target.value)} className="input-field">
                {['MALE', 'FEMALE', 'OTHER'].map(g => <option key={g} value={g}>{g}</option>)}
              </select>
            </div>
            {error && (
              <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-500 text-xs font-mono">
                {error}
              </div>
            )}
          </div>
        )}

        {/* Step 2: Initial offence */}
        {step === 2 && (
          <div className="space-y-3">
            <div>
              <label className="block text-xs font-mono text-gray-500 uppercase tracking-wider mb-1">Offence Type</label>
              <input type="text" value={form.offenceType} onChange={e => set('offenceType', e.target.value)} placeholder="e.g. Armed Robbery" className="input-field" />
            </div>
            <div>
              <label className="block text-xs font-mono text-gray-500 uppercase tracking-wider mb-1">Incident Date</label>
              <input type="date" value={form.offenceDate} onChange={e => set('offenceDate', e.target.value)} className="input-field" />
            </div>
            <div>
              <label className="block text-xs font-mono text-gray-500 uppercase tracking-wider mb-1">Location</label>
              <input type="text" value={form.offenceLocation} onChange={e => set('offenceLocation', e.target.value)} placeholder="e.g. Mushin, Lagos" className="input-field" />
            </div>
          </div>
        )}

        {/* Nav buttons */}
        <div className="flex gap-3 mt-5">
          {step > 0 && (
            <button onClick={() => setStep(s => s - 1)} className="flex-1 py-3 text-sm border border-border-color-light dark:border-border-color rounded-xl text-gray-500 hover:bg-gray-100 dark:hover:bg-white/5 transition-colors flex items-center justify-center gap-2">
              <ArrowLeft className="w-4 h-4" /> Back
            </button>
          )}
          {step < STEPS.length - 1 ? (
            <button onClick={() => setStep(s => s + 1)} className="flex-1 btn-primary py-3 text-sm font-semibold flex items-center justify-center gap-2">
              Next <ArrowRight className="w-4 h-4" />
            </button>
          ) : (
            <button onClick={handleSubmit} disabled={loading} className="flex-1 btn-primary py-3 text-sm font-semibold flex items-center justify-center gap-2 disabled:opacity-60">
              {loading ? <><Loader2 className="w-4 h-4 animate-spin" /> Saving...</> : <><CheckCircle className="w-4 h-4" /> Save Record</>}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
