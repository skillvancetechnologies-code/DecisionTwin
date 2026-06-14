# DecisionTwin — Frontend (React + Vite)

Single-page app: landing, CSV upload, baseline dashboard, simulation,
streaming copilot chat, and a scenario comparison dashboard.

## Stack

React 19 · Vite · TailwindCSS 3 (frozen design tokens) · React Router 6 ·
Zustand · Recharts · TanStack Table · react-dropzone · react-markdown ·
Papaparse / jsPDF / html2canvas (client-side export) · axios.

## Develop

```bash
npm install
cp .env.example .env.local   # VITE_API_BASE_URL=http://localhost:8000/v1
npm run dev                  # http://localhost:5173
npm run build                # production build → dist/
npm run lint
```

## Structure

```
src/
  api/           client + datasets/simulate/chat/scenarios
  components/     layout · forms · cards · chat · charts · dashboard · scenario · ui
  hooks/          useDataset · useSimulation · useChatStream
  lib/            formatters · exporters/{csv,pdf}
  pages/          Landing · Upload · Baseline · Simulate · Chat · Dashboard · NotFound
  store/          appStore (Zustand)
  styles/         tailwind.css
```

## Routes

`/` · `/upload` · `/baseline/:datasetId` · `/simulate/:datasetId` ·
`/chat/:sessionId` · `/dashboard` · `*` (404)

## Deploy (Vercel)

Set `VITE_API_BASE_URL` to the deployed backend `/v1` URL. SPA fallback routing
is configured in `vercel.json`.
