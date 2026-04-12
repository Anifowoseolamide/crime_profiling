export const userProfiles = [
  {
    badgeId: "1024-FO",
    password: "password123",
    role: "FIELD_OFFICER",
    name: "Sgt. Ibrahim Musa",
    rank: "Sergeant",
    station: "Ikeja Area F",
    accessLevel: 1
  },
  {
    badgeId: "2048-SV",
    password: "password123",
    role: "SUPERVISOR",
    name: "Insp. Funke Adebayo",
    rank: "Inspector",
    station: "Lagos State Command",
    accessLevel: 2
  },
  {
    badgeId: "9999-AD",
    password: "password123",
    role: "ADMIN",
    name: "Comm. Chinedu Eze",
    rank: "Commissioner of Police",
    station: "HQ",
    accessLevel: 3
  }
];

export const subjects = [
  {
    id: "SUBJ-L-99821",
    name: "Kingsley Odua",
    aliases: ["K-Boy", "Slick"],
    status: "WANTED",
    priority: "CRITICAL",
    lastSeen: "2026-04-09T14:30:00Z",
    location: "Oshodi Underbridge",
    coordinates: { lat: 6.5540, lng: 3.3444 },
    confidence: 96.5,
    warrantDetails: {
      issuedBy: "Lagos High Court",
      date: "2026-04-01",
      reason: "Armed Robbery, Assault"
    },
    offences: [
      { code: "OFF-112", type: "Armed Robbery", date: "2026-03-15", officer: "Sgt. Ibrahim Musa", location: "Mushin" },
      { code: "OFF-110", type: "Assault", date: "2025-12-02", officer: "Cpl. John Mark", location: "Surulere" }
    ],
    timeline: [
      { type: "ARREST", date: "2023-05-10", notes: "Arrested for grand theft" },
      { type: "REPORT", date: "2025-12-02", notes: "Reported involved in street brawl" },
      { type: "WARRANT", date: "2026-04-01", notes: "Warrant issued for armed robbery" }
    ],
    mugshotUrl: "https://ui-avatars.com/api/?name=Kingsley+Odua&background=333&color=fff&size=512&rounded=true"
  },
  {
    id: "SUBJ-L-45123",
    name: "Babatunde Shola",
    aliases: ["Baba"],
    status: "WATCHLIST",
    lastSeen: "2026-04-05T09:15:00Z",
    location: "Agege Area",
    coordinates: { lat: 6.6186, lng: 3.3215 },
    confidence: 88.2,
    offences: [
      { code: "OFF-088", type: "Fraud - Cyber", date: "2024-08-20", officer: "Insp. Funke Adebayo", location: "Victoria Island" }
    ],
    timeline: [
      { type: "REPORT", date: "2024-08-20", notes: "Questioned regarding wire fraud scheme" },
      { type: "SIGHTING", date: "2026-04-05", notes: "Spotted via CCTV in Agege" }
    ],
    mugshotUrl: "https://ui-avatars.com/api/?name=Babatunde+Shola&background=333&color=fff&size=512&rounded=true"
  },
  {
    id: "SUBJ-L-11287",
    name: "Chioma Nnadi",
    aliases: ["CeeCee"],
    status: "CLEARED",
    lastSeen: "2025-10-12T11:00:00Z",
    location: "Lekki Phase 1",
    coordinates: { lat: 6.4475, lng: 3.4735 },
    confidence: 99.1,
    offences: [],
    timeline: [
      { type: "ARREST", date: "2022-01-15", notes: "Wrongful identification, released immediately" },
      { type: "REPORT", date: "2025-10-12", notes: "Cleared of all suspicion in Lekki incident" }
    ],
    mugshotUrl: "https://ui-avatars.com/api/?name=Chioma+Nnadi&background=333&color=fff&size=512&rounded=true"
  }
];

export const auditLogs = [
  { id: "LOG-001", timestamp: "2026-04-10T15:05:22Z", officer: "1024-FO", action: "FIELD_SCAN", subject: "SUBJ-L-99821", ip: "192.168.1.45" },
  { id: "LOG-002", timestamp: "2026-04-10T14:30:10Z", officer: "2048-SV", action: "ISSUE_WARRANT", subject: "SUBJ-L-99821", ip: "10.0.0.12" },
  { id: "LOG-003", timestamp: "2026-04-10T12:15:00Z", officer: "1024-FO", action: "VIEW_PROFILE", subject: "SUBJ-L-45123", ip: "192.168.1.45" },
];
