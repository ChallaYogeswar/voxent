# EchoForge Frontend

Advanced Speaker Diarization Platform - React Frontend

## Project Structure

```
echoforge-frontend/
├── src/
│   ├── components/         # Reusable components
│   │   ├── Navbar.jsx
│   │   ├── Hero.jsx
│   │   ├── UploadSection.jsx
│   │   ├── ProcessingStatus.jsx
│   │   ├── ResultsDisplay.jsx
│   │   └── ProtectedRoute.jsx
│   ├── pages/             # Page components
│   │   ├── LandingPage.jsx
│   │   ├── LoginPage.jsx
│   │   ├── RegisterPage.jsx
│   │   └── DashboardPage.jsx
│   ├── context/           # Global state
│   │   └── AuthContext.jsx
│   ├── services/          # API calls
│   │   └── api.js
│   ├── utils/             # Utilities
│   │   ├── constants.js
│   │   └── helpers.js
│   ├── App.jsx
│   ├── index.js
│   └── index.css
├── public/
│   └── index.html
├── .env                   # Development environment
├── .env.production        # Production environment
├── package.json
├── tailwind.config.js
├── postcss.config.js
└── README.md
```

## Installation

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables:
```bash
# .env (Development)
REACT_APP_API_URL=http://localhost:5000

# .env.production (Production)
REACT_APP_API_URL=https://api.echoforge.io
```

3. Start development server:
```bash
npm start
```

4. Build for production:
```bash
npm run build
```

## Features

- **User Authentication**: Register, login, and session management
- **Audio Upload**: Support for WAV, MP3, M4A, FLAC (up to 500MB)
- **Real-time Processing**: Live status updates with progress tracking
- **Speaker Diarization**: AI-powered speaker identification and separation
- **Results Management**: Download speaker audio and detailed metrics
- **Responsive Design**: Works on desktop, tablet, and mobile

## API Integration

The frontend integrates with the EchoForge backend API with the following endpoints:

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/verify` - Token verification

### Processing
- `POST /upload` - Upload audio file
- `GET /status/<job_id>` - Check processing status
- `GET /download/<job_id>/<speaker_id>` - Download speaker audio
- `GET /download/<job_id>/metadata.json` - Download metadata

See [API Contract](../TO%20DO/voxent%20upgradation.md) for complete specifications.

## Technologies

- React 18+ with Hooks
- React Router 6 for navigation
- Tailwind CSS for styling
- Axios for API calls
- Context API for state management

## Best Practices

- **Error Handling**: All API calls include error boundaries
- **Loading States**: Visual feedback during async operations
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Security**: JWT token management and automatic logout on 401
- **Performance**: Code splitting and lazy loading where applicable

## Development Checklist

- [x] Project structure setup
- [x] Components implementation
- [x] API service layer
- [x] Authentication context
- [x] Routing and navigation
- [x] Tailwind CSS configuration
- [ ] Unit tests
- [ ] Integration tests
- [ ] Performance optimization
- [ ] Accessibility testing
- [ ] Browser compatibility testing

## Deployment

See [Deployment Checklist](../TO%20DO/voxent%20upgradation.md) for production deployment guidelines.

## Support

For issues, feature requests, or contributions, please refer to the project documentation.
