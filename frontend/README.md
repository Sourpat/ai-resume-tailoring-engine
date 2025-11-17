# Frontend

## Environment

Create a `.env.local` file (or copy `.env.local.example`) and set the backend URL:

```
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

The value should point to wherever the backend API is running.

## Running the stack

1. Start the backend (from the repository root):
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
2. Start the frontend in another terminal:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
3. Open the frontend at http://localhost:3000 and ensure the API URL matches the backend host/port.
