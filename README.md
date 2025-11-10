# Pokemon Card Scanner

A mobile app for scanning Pokemon cards and retrieving real-time pricing information from multiple sources.

## Current Status: MVP Complete ✅

**Working Features:**
- ✅ Image upload and selection
- ✅ Backend API processing 
- ✅ Results display with scanned image
- ✅ Multiple price sources (TCGPlayer, CardMarket)
- ✅ Price statistics (median, average)
- ✅ Clean, professional UI
- ✅ End-to-end flow tested with stub data

**Running in Stub Mode:**
- OCR: Returns mock Charizard card data
- Pricing: Returns mock prices ($95-$125)
- Allows testing without API credentials

## Quick Start

### Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Backend runs at: http://192.168.50.229:8000 (WSL2 IP for Windows browser access)

### Frontend (React Native + Expo)
```bash
cd mobile
npm install
npm run web
```

Frontend runs at: http://localhost:8081

## Project Structure

```
pokemon-card-scanner/
├── backend/              # FastAPI server
│   ├── api/             # API routes
│   ├── clients/         # External API clients (Google Vision, Pokemon TCG)
│   ├── services/        # Business logic (OCR, pricing)
│   ├── models/          # Pydantic schemas
│   ├── utils/           # Error handlers
│   ├── main.py          # FastAPI app entry point
│   ├── config.py        # Configuration
│   └── Dockerfile       # Docker config for Cloud Run
│
└── mobile/              # React Native app
    ├── src/
    │   ├── screens/     # CameraScreen, ResultsScreen
    │   ├── services/    # API client
    │   └── types/       # TypeScript types
    ├── App.tsx          # App entry point
    └── package.json     # Dependencies
```

## Technical Details

### Backend
- **Framework:** FastAPI
- **OCR:** Google Cloud Vision API (stub mode active)
- **Pricing:** Pokemon TCG API (stub mode active)
- **CORS:** Configured for WSL2 cross-origin requests
- **Image Upload:** Multipart form-data with File objects

### Frontend
- **Framework:** React Native with Expo
- **Platforms:** iOS, Android, Web
- **Image Handling:** expo-image-picker
- **API Client:** axios with File object serialization
- **Navigation:** React Navigation

### Key Fixes Applied
1. **CORS:** Set `allow_origins=["*"]` for development
2. **Image Upload:** Use File objects instead of Blobs for axios compatibility
3. **Stub Mode:** Returns mock data when APIs unavailable
4. **Navigation:** Pass image URI to results screen

## How to Use

1. **Start Backend:** `cd backend && uvicorn main:app --host 0.0.0.0 --port 8000`
2. **Start Frontend:** `cd mobile && npm run web`
3. **Open Browser:** http://localhost:8081
4. **Upload Image:** Click "Select Photo" and choose any image
5. **Scan:** Click "Scan Card"
6. **View Results:** See the image + mock Charizard pricing data

## Next Steps

### To Use Real APIs:

1. **Google Cloud Vision:**
   - Create service account key
   - Download JSON credentials
   - Set `GOOGLE_APPLICATION_CREDENTIALS` in `.env`

2. **Pokemon TCG API:**
   - Get API key from https://pokemontcg.io
   - Set `POKEMON_TCG_API_KEY` in `.env`

3. **Restart Backend:**
   - Services will automatically use real APIs instead of stubs

### To Deploy to Cloud Run:

```bash
cd backend
gcloud run deploy pokemon-card-scanner \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

Then update `mobile/src/services/api.ts` with the Cloud Run URL.

## Debugging

### Backend Logs
```bash
tail -f /tmp/backend.log
```

### Frontend Logs
- Open browser DevTools (F12)
- Check Console tab for `[API]` and `[CameraScreen]` logs

### Common Issues

**400 Bad Request:**
- Check that File objects (not Blobs) are being sent
- Verify CORS headers in network tab

**No Results Displayed:**
- Check browser console for errors
- Verify backend is running: `curl http://192.168.50.229:8000/api/v1/health`

**Image Not Showing:**
- Ensure `imageUri` is passed through navigation
- Check that Image component has proper source prop

## Repository

https://github.com/tonton2006/pokemon-card-scanner

## Built With

- FastAPI
- React Native + Expo
- Google Cloud Vision API
- Pokemon TCG API
- Google Cloud Run (ready to deploy)

---

🤖 Built with Claude Code
