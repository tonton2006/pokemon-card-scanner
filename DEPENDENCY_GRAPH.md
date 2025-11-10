# Task Dependency Graph - Pokemon Card Scanner MVP

**Visual representation of task dependencies and execution flow**

---

## Critical Path (Longest Chain - 6 Weeks)

```
START
  |
  v
T001 (Project Structure) [15min]
  |
  +---> T002 (React Native Init) [1h]
  |       |
  |       v
  |     T003 (RN Dependencies) [45min]
  |       |
  |       +---> T004 (ESLint/Prettier) [30min]
  |       |
  |       v
  |     T011 (Navigation Setup) [1h]
  |       |
  |       v
  |     T012 (Camera Permissions) [1.5h]
  |       |
  |       v
  |     T013 (Camera Screen) [3h] *** CRITICAL PATH ***
  |       |
  |       v
  |     T014 (Image Capture) [2h] *** CRITICAL PATH ***
  |       |
  |       v
  |     T019 (Image Validation) [1h]
  |       |
  |       v
  |     T041 (API Client) [2h] (waits for T036 backend)
  |       |
  |       v
  |     T042 (Scan Flow Integration) [3h] *** CRITICAL PATH ***
  |       |
  |       v
  |     T043 (Results Screen) [3h] *** CRITICAL PATH ***
  |       |
  |       v
  |     T044 (Loading States) [1.5h]
  |       |
  |       v
  |     T052 (Production URL Config) [30min] *** CRITICAL PATH ***
  |       |
  |       v
  |     T054 (Performance Optimization) [3h] *** CRITICAL PATH ***
  |       |
  |       v
  |     T055 (E2E Testing) [4h] *** CRITICAL PATH ***
  |       |
  |       v
  |     T056 (Bug Fixes) [4h] *** CRITICAL PATH ***
  |       |
  |       +---> T060 (iOS Release) [2h]
  |       |
  |       +---> T061 (Android Release) [2h]
  |
  v
END (MVP Launch)
```

**Critical Path Duration**: ~37 hours of sequential work

---

## Parallel Work Streams

### Stream 1: Mobile Foundation & UI (Week 1-2)

```
T001
  |
  v
T002 --> T003 --> T011 --> T015 (Home Screen) [2h]
              |        |
              |        +-> T016 (Loading Components) [1.5h]
              |        |
              |        +-> T017 (Results Placeholder) [2h]
              |        |
              |        +-> T018 (Error Handling UI) [1.5h]
              |
              v
            T004 (ESLint/Prettier)
              |
              v
            T012 --> T013 --> T014 --> T019
                                    |
                                    v
                                  T020 (Unit Tests) [2h]
```

**Can run parallel**: T015, T016, T017, T018 (all depend on T011)

---

### Stream 2: Backend Foundation (Week 1-4)

```
T001
  |
  v
T005 (FastAPI Init) [1h]
  |
  v
T006 (Backend Dependencies) [30min]
  |
  +---> T021 (OCR Service) [2h]
  |       |
  |       v
  |     T022 (Text Detection Endpoint) [2h]
  |       |
  |       v
  |     T023 (Card Parser) [4h]
  |       |
  |       +---> T025 (OCR Response Format) [1h]
  |       |       |
  |       |       v
  |       |     T026 (OCR Error Handling) [1.5h]
  |       |       |
  |       |       v
  |       |     T029 (Unit Tests OCR) [2h]
  |       |
  |       v
  |     T028 (OCR Optimization) [3h]
  |       |
  |       v
  |     T030 (Integration Tests OCR) [2h]
  |
  +---> T024 (Card Data Model) [1h] (can run parallel with T021)
  |
  +---> T032 (TCG API Service) [2h]
          |
          v
        T033 (Card Search Endpoint) [2h]
          |
          +---> T037 (Caching) [2h]
          |
          +---> T038 (Rate Limiting) [1.5h]
          |
          v
        T034 (Pricing Aggregation) [2h]
          |
          v
        T035 (Pricing Model) [1h]
          |
          v
        T036 (Combined Scan Endpoint) [2h] *** INTEGRATION POINT ***
          |
          v
        T039 (Unit Tests Pricing) [2h]
          |
          v
        T040 (API Documentation) [1.5h]
```

**Parallel opportunity**: T024 can be built while T021-T023 are in progress

---

### Stream 3: Cloud Infrastructure (Week 1, Week 6)

```
T007 (GCP Project Setup) [30min] (INDEPENDENT - can start immediately)
  |
  v
T008 (Service Account) [20min]
  |
  v
(Used by T021 for OCR, T050 for deployment)


Later (Week 6):

T036 (Backend complete)
  |
  v
T049 (Dockerfile) [1.5h]
  |
  v
T050 (Deploy to Cloud Run) [2h] *** DEPLOYMENT GATE ***
  |
  v
T051 (Configure Environment) [1h]
  |
  +---> T058 (Monitoring/Logging) [2h]
  |
  v
(Enables T052 production config)
```

**T007-T008 can run completely in parallel with T001-T006**

---

### Stream 4: Research & Documentation (Throughout)

```
Week 3 (parallel with OCR dev):
T027 (Pokemon Card OCR Research) [3h] (INDEPENDENT)
  |
  v
(Informs T028 optimization)
  |
  v
(Provides test dataset for T030, T055)


Week 4 (parallel with pricing dev):
T031 (TCG API Research) [2h] (INDEPENDENT)
  |
  v
(Informs T032-T034)


Week 1, 6 (documentation):
T010 (Dev Documentation) [45min]
T057 (User Documentation) [2h]
T062 (Project Retrospective) [2h]
```

---

## Phase-by-Phase Dependency View

### Phase 1: Week 1 (Foundation)

```
START --> T001 (Project Structure)
            |
            +---> T002 --> T003 --> T004
            |               |
            |               v
            |             T009 (Env Templates)
            |
            +---> T005 --> T006 --> T009
            |
            +---> T007 --> T008
            |
            v
          T010 (Dev Docs)
```

**Blockers**: T001 blocks most of Phase 1

**Parallel**: T007 (GCP) is fully independent

---

### Phase 2: Week 2 (Camera & UI)

```
T003 --> T011 (Navigation)
           |
           +---> T015 (Home Screen) \
           |                          \
           +---> T016 (Loading)        } Can run in parallel
           |                          /
           +---> T017 (Results UI)   /
           |                        /
           +---> T018 (Error UI) __/
           |
           v
         T012 (Camera Permissions)
           |
           v
         T013 (Camera Screen) *** Takes 3 hours ***
           |
           v
         T014 (Image Capture)
           |
           +---> T019 (Image Validation)
           |
           v
         T020 (Unit Tests)
```

**Critical**: T013 is on critical path (3 hours)

**Parallel**: T015-T018 can all run simultaneously after T011

---

### Phase 3: Week 3 (OCR)

```
T027 (Research) -- Independent, can start anytime

T006 --> T021 (OCR Service)
           |
           +---> T024 (Card Model) - can run parallel
           |
           v
         T022 (OCR Endpoint)
           |
           v
         T023 (Card Parser) *** Takes 4 hours ***
           |
           v
         T025 (Response Format)
           |
           v
         T026 (Error Handling)
           |
           v
         T028 (Optimization) *** Needs T027 research ***
           |
           +---> T029 (Unit Tests)
           |
           v
         T030 (Integration Tests)
```

**Critical**: T023 parser takes 4 hours

**Dependency**: T028 optimization needs T027 research completed

---

### Phase 4: Week 4 (Pricing)

```
T031 (TCG API Research) -- Independent

T024 --> T032 (TCG Service) *** Needs T031 research ***
           |
           v
         T033 (Search Endpoint)
           |
           +---> T037 (Caching)
           |
           +---> T038 (Rate Limiting)
           |
           v
         T034 (Pricing Aggregation)
           |
           v
         T035 (Pricing Model)

T025 (OCR) + T034 (Pricing) --> T036 (Combined Endpoint) *** INTEGRATION ***
                                  |
                                  +---> T039 (Unit Tests)
                                  |
                                  v
                                T040 (API Docs)
```

**Integration Point**: T036 combines OCR + Pricing (critical)

**Parallel**: T037, T038 can be developed alongside T034

---

### Phase 5: Week 5 (Integration)

```
T036 (Backend Complete) + T003 (Mobile Foundation)
  |
  v
T041 (API Client Service)
  |
  v
T014 --> T042 (Scan Flow Integration) *** Takes 3 hours ***
           |
           v
         T043 (Results with Real Data) *** Takes 3 hours ***
           |
           +---> T044 (Loading States)
           |
           +---> T045 (Error Handling)
           |
           +---> T046 (Scan History)
           |
           v
         T047 (Upload Optimization)
           |
           v
         T048 (Integration Tests)
```

**Critical**: T042 and T043 are sequential and on critical path (6 hours total)

**Parallel**: T044-T046 can run after T043

---

### Phase 6: Week 6 (Deployment & Polish)

```
T036 --> T049 (Dockerfile)
           |
           v
T008 --> T050 (Deploy to Cloud Run) *** DEPLOYMENT GATE ***
           |
           v
         T051 (Configure Environment)
           |
           +---> T058 (Monitoring) - can run parallel
           |
           v
         T041 --> T052 (Production URL)
                    |
                    +---> T053 (UI/UX Polish) - can run parallel
                    |
                    v
                  T054 (Performance Optimization)
                    |
                    v
                  T055 (E2E Testing) *** Takes 4 hours ***
                    |
                    v
                  T056 (Bug Fixes) *** Takes 4 hours ***
                    |
                    +---> T060 (iOS Release) \
                    |                          } Can run in parallel
                    +---> T061 (Android Release) /
                    |
                    v
                  T059 (Security Review) - can run parallel
                    |
                    v
                  T057 (User Docs)
                    |
                    v
                  T062 (Retrospective)
```

**Critical**: T055 and T056 are sequential (8 hours on critical path)

**Parallel**: T053, T058, T059 can run simultaneously

**Final Parallel**: T060 and T061 (iOS/Android builds)

---

## Bottleneck Analysis

### Top Time-Consuming Tasks (Sequential)
1. **T056** - Bug Fixes (4 hours) - Week 6
2. **T055** - E2E Testing (4 hours) - Week 6
3. **T023** - Card Parser (4 hours) - Week 3
4. **T028** - OCR Optimization (3 hours) - Week 3
5. **T013** - Camera Screen (3 hours) - Week 2
6. **T043** - Results Screen (3 hours) - Week 5
7. **T042** - Scan Integration (3 hours) - Week 5

**Total bottleneck time**: 24 hours on critical path

### High-Dependency Tasks (Blocking Many)
1. **T001** - Blocks 18 tasks directly/indirectly
2. **T011** - Blocks all UI screens (T015-T018)
3. **T036** - Blocks mobile integration (T041-T048)
4. **T050** - Blocks production deployment (T052-T062)

### Integration Points (Risk Areas)
1. **T036** - Combines OCR + Pricing (Week 4)
2. **T042** - Mobile + Backend integration (Week 5)
3. **T050** - Deployment to production (Week 6)

---

## Parallelization Strategy

### Maximum Parallelization Opportunities

**Week 1 (Phase 1):**
```
In parallel:
- T007 → T008 (GCP setup)
- T001 → T002 → T003, T004 (Mobile)
- T001 → T005 → T006 (Backend)
```
**Agents needed**: 2-3 simultaneously

**Week 2 (Phase 2):**
```
In parallel after T011:
- T015 (Home Screen)
- T016 (Loading Components)
- T017 (Results Placeholder)
- T018 (Error UI)

Sequential (critical path):
- T012 → T013 → T014 → T019
```
**Agents needed**: Up to 4 simultaneously for UI work

**Week 3 (Phase 3):**
```
In parallel:
- T027 (Research)
- T021 → T022 → T023 (OCR pipeline)
- T024 (Data model)
```
**Agents needed**: 2-3 simultaneously

**Week 6 (Phase 6):**
```
In parallel after T050:
- T053 (UI Polish)
- T058 (Monitoring)
- T059 (Security Review)

Final parallel:
- T060 (iOS Release)
- T061 (Android Release)
```
**Agents needed**: Up to 3 simultaneously

---

## Resource Allocation Recommendations

### Week-by-Week Agent Assignment

**Week 1**: 3 agents
- Agent 1: Mobile setup (T002-T004)
- Agent 2: Backend setup (T005-T006)
- Agent 3: Cloud setup (T007-T008)

**Week 2**: 2 agents
- Agent 1: Camera flow (T012-T014, critical path)
- Agent 2: UI screens (T015-T018, parallel)

**Week 3**: 2 agents
- Agent 1: OCR implementation (T021-T026)
- Agent 2: OCR optimization (T027-T030)

**Week 4**: 1-2 agents
- Agent 1: Pricing backend (T032-T036)
- Agent 2: Caching/optimization (T037-T040)

**Week 5**: 1-2 agents
- Agent 1: Integration work (T041-T043, critical)
- Agent 2: Optimization (T044-T048)

**Week 6**: 3 agents
- Agent 1: Deployment (T049-T052)
- Agent 2: Testing & fixes (T055-T056, critical)
- Agent 3: Polish & documentation (T053, T057-T059)

---

## Quick Reference: What Can Start Now?

### Immediate (No Dependencies)
- **T001** - Project Structure (15 min)
- **T007** - GCP Project Setup (30 min)

### After T001 (15 minutes)
- **T002** - React Native Init (1 hour)
- **T005** - FastAPI Init (1 hour)

### After 2 Hours (T001 + T002/T005)
- **T003** - RN Dependencies (45 min)
- **T006** - Backend Dependencies (30 min)

### After ~3 Hours
- **T004** - ESLint/Prettier (30 min)
- **T011** - Navigation (1 hour)
- **T009** - Environment Templates (15 min)

---

*This dependency graph should be used to identify parallel work opportunities and avoid blocking the critical path.*
