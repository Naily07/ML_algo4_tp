import { NextResponse } from 'next/server';

// POST /api/best-move
export async function POST(request: Request) {
  try {
    const { board } = await request.json();
    // Appel à l'API backend (remplacez l'URL par celle de votre backend)
    const backendUrl = 'http://localhost:5000/api/best-move';
    const backendRes = await fetch(backendUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ board }),
    });
    if (!backendRes.ok) {
      return NextResponse.json({ error: 'Erreur backend' }, { status: 500 });
    }
    const data = await backendRes.json();
    // On suppose que data.bestMove est l'index du meilleur coup
    return NextResponse.json({ bestMove: data.bestMove });
  } catch {
    return NextResponse.json({ error: 'Erreur serveur' }, { status: 500 });
  }
}
