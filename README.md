# Pokemon Card Scanner

MVP mobile app for scanning Pokemon cards and getting real-time pricing from multiple sources.

## Features (MVP)

- 📸 Scan Pokemon cards with your phone camera
- 💰 Get pricing from multiple sources (TCGPlayer, eBay, CardMarket)
- 📊 See median/average pricing recommendations
- 🚀 Fast results in 2-3 seconds

## Tech Stack

- **Mobile**: React Native (iOS + Android)
- **OCR**: Google Cloud Vision API
- **Pricing**: Pokemon TCG API + additional sources
- **Backend**: FastAPI (Python)
- **Deployment**: Google Cloud Run

## Project Structure

```
pokemon-card-scanner/
├── mobile/              # React Native app
├── backend/             # FastAPI pricing service
├── docs/                # Architecture and design docs
└── research/            # Research findings and data
```

## Development Timeline

- Week 1-2: Setup & Camera
- Week 3: Card Detection & OCR
- Week 4: Pricing Backend
- Week 5: Frontend-Backend Integration
- Week 6: Polish & Testing

## Getting Started

Coming soon...

## License

MIT
