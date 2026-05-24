const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const request = async (endpoint, options = {}) => {
  const token = localStorage.getItem('lagoscp_token');
  const csrfToken = getCookie('csrftoken');
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...(csrfToken && { 'X-CSRFToken': csrfToken }),
    ...options.headers,
  };

  const response = await fetch(`${BASE_URL}${endpoint}`, { 
    ...options, 
    headers,
    credentials: 'include' 
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || errorData.error || errorData.non_field_errors?.[0] || 'API request failed');
  }
  
  if (response.status === 204) return null;
  return response.json();
};

export const api = {
  login: async (badgeId, password) => {
    const res = await request('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ badge_number: badgeId, password })
    });
    // the backend uses 'officer', we map to 'user' for context compatibility
    return {
      token: res.access,
      user: {
        ...res.officer,
        name: res.officer.full_name,
        badgeId: res.officer.badge_number,
        accessLevel: res.officer.role === 'ADMIN' ? 3 : (res.officer.role === 'SUPERVISOR' ? 2 : 1)
      }
    };
  },

  identifyFace: async (base64Image, location, coords) => {
    const res = await request('/identify/', {
      method: 'POST',
      body: JSON.stringify({
        image: base64Image,
        location: location,
        latitude: coords?.lat,
        longitude: coords?.lng
      })
    });
    
    let subject = res.subject;
    if (subject) {
      subject.name = `${subject.first_name || ''} ${subject.last_name || ''}`.trim();
      // Add rich metadata needed for scan result modals
      subject.confidence = res.confidence ? Math.round(res.confidence) : 0;
      if (res.warrant) {
        subject.warrantDetails = {
          issuedBy: res.warrant.issuing_authority || 'Lagos CP',
          date: res.warrant.issued_date,
          reason: res.warrant.reason
        };
      }
    }
    
    return {
      match: res.match_found,
      subject: subject
    };
  },

  getSubject: async (id) => {
    const subject = await request(`/subjects/${id}/`);
    subject.name = `${subject.first_name || ''} ${subject.last_name || ''}`.trim();
    
    // Fetch offences
    try {
      const rawOffences = await request(`/offences/?subject_id=${id}`);
      const offenceList = rawOffences.results || rawOffences;
      subject.offences = Array.isArray(offenceList) ? offenceList.map(o => ({
         code: o.offence_code || String(o.id).substring(0, 8),
         type: o.offence_category,
         date: o.incident_date,
         location: o.location,
         officer: o.arresting_officer?.full_name || 'System'
      })) : [];
    } catch (e) {
      subject.offences = [];
    }

    // Fetch timeline
    try {
      subject.timeline = await request(`/subjects/${id}/timeline/`);
    } catch (e) {
      subject.timeline = [];
    }

    // Fetch active warrants to satisfy warrantDetails format
    try {
      const activeWarrants = await request(`/wanted/?subject_id=${id}&is_active=true`);
      const warrants = activeWarrants.results || activeWarrants;
      if (Array.isArray(warrants) && warrants.length > 0) {
         const latest = warrants[0];
         subject.warrantDetails = {
             issuedBy: latest.issuing_authority || 'Lagos CP',
             date: latest.issued_date,
             reason: latest.reason
         };
      }
    } catch(e) { }

    return subject;
  },

  updateSubject: async (id, data) => {
    return request(`/subjects/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(data)
    });
  },

  searchSubjects: async (queryStr = "", statusFilter = "ALL") => {
    let url = `/subjects/?search=${encodeURIComponent(queryStr)}`;
    if (statusFilter !== "ALL") {
      url += `&status=${encodeURIComponent(statusFilter)}`;
    }
    const res = await request(url);
    const results = res.results || res;
    return Array.isArray(results) ? results.map(s => ({
      ...s,
      name: `${s.first_name || ''} ${s.last_name || ''}`.trim()
    })) : [];
  },

  getWantedList: async () => {
    const res = await request('/wanted/?is_active=true');
    const warrants = res.results || res;
    if (!Array.isArray(warrants)) return [];
    
    // Deduplicate subjects by ID (one person might have multiple warrants)
    const uniqueSubjects = new Map();
    warrants.forEach(w => {
      const s = w.subject;
      if (s && !uniqueSubjects.has(s.id)) {
        s.name = `${s.first_name || ''} ${s.last_name || ''}`.trim();
        uniqueSubjects.set(s.id, s);
      }
    });
    
    return Array.from(uniqueSubjects.values());
  },

  getAuditLog: async () => {
    return request('/audit/feed/');
  },
  
  getAuditList: async (page = 1) => {
    return request(`/audit/?page=${page}`);
  },
  
  getStations: async () => {
    return request('/auth/stations/');
  },

  createSubject: async (data) => {
    return request('/subjects/', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  },

  enrolMugshot: async (subjectId, imageBase64, coords = null) => {
    return request(`/subjects/${subjectId}/enrol-mugshot/`, {
      method: 'POST',
      body: JSON.stringify({ 
        image: imageBase64,
        latitude: coords?.lat,
        longitude: coords?.lng
      })
    });
  },
  
  logOffence: async (data) => {
    // Map frontend's {subjectId, type, date, location, notes, stationId, latitude, longitude} to backend Offence payload
    const payload = {
      subject_id: data.subjectId,
      station_id: data.stationId,
      offence_category: 'OTHER',
      offence_title: `${data.type} at ${data.location}`,
      description: data.notes || '',
      severity: 'MODERATE',
      incident_date: data.date ? new Date(data.date).toISOString() : new Date().toISOString(),
      location: data.location,
      latitude: data.latitude,
      longitude: data.longitude
    };
    
    // Attempt basic mapping
    const catMap = {
      'Armed Robbery': 'ARMED_ROBBERY', 'Assault': 'ASSAULT',
      'Fraud - Cyber': 'CYBERCRIME', 'Fraud - Financial': 'FRAUD',
      'Drug Trafficking': 'DRUGS', 'Murder': 'HOMICIDE',
      'Kidnapping': 'KIDNAPPING', 'Theft': 'THEFT'
    };
    if (catMap[data.type]) {
      payload.offence_category = catMap[data.type];
    }
    
    const res = await request('/offences/', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
    return { success: true, offenceCode: res.offence_code || res.id };
  },

  getHotspots: async () => {
    return request('/offences/hotspots/');
  },

  getStats: async () => {
    return request('/audit/stats/');
  },

  declareWanted: async (data) => {
    const today = new Date().toISOString().split('T')[0];
    return request('/wanted/', {
      method: 'POST',
      body: JSON.stringify({
        subject_id: data.subjectId,
        warrant_number: data.warrantNumber,
        issuing_authority: data.issuingAuthority,
        reason: data.reason,
        priority: data.priority,
        issued_date: today,
        expiry_date: data.expiryDate || null
      })
    });
  }
};
