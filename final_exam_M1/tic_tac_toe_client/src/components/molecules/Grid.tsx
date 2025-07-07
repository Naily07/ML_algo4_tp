'use client';

import React, { useState } from 'react';
import Image from 'next/image';

const initialBoard = Array(9).fill(null);

const getWinner = (board: (string | null)[]) => {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (board[a] && board[a] === board[b] && board[a] === board[c]) {
      return { winner: board[a], line: lines[i], lineIndex: i };
    }
  }
  return null;
};

const convertBoardForAPI = (board: (string | null)[]) => {
  // X = 1, O = -1, null = 0
  return board.map((cell) => (cell === 'X' ? 1 : cell === 'O' ? -1 : 0));
};

const getBestMove = async (board: (string | null)[]) => {
  const apiBoard = convertBoardForAPI(board);
  console.log(apiBoard);

  try {
    const response = await fetch(process.env.NEXT_PUBLIC_API_URL + '/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ board: apiBoard }),
    });
    console.log('Response from API:', response);
    if (!response.ok) throw new Error('Erreur API');
    const data = await response.json();
    console.log('Data from API:', data);
    return data.proposed_move;
  } catch (error) {
    console.error('Erreur lors de la récupération du meilleur coup:', error);
    return null;
  }
};

const Grid = () => {
  const [board, setBoard] = useState<(string | null)[]>(initialBoard);
  const [xIsNext, setXIsNext] = useState(true);
  const winnerObj = getWinner(board);
  const winner = winnerObj?.winner || null;
  const [result, setResult] = useState<string | null>(null);

  const handleClick = async (idx: number) => {
    if (board[idx] || winner) return;
    const newBoard = board.slice();
    newBoard[idx] = xIsNext ? 'X' : 'O';
    setBoard(newBoard);
    setXIsNext(!xIsNext);
    const winnerCheck = getWinner(newBoard);
    if (winnerCheck) {
      setResult(winnerCheck.winner);
      return;
    } else if (newBoard.every((cell) => cell)) setResult('Draw');
    // Appel à l'API pour obtenir le meilleur coup
    const bestMove = await getBestMove(newBoard);
    if (xIsNext) {
      console.log('Meilleur coup:', bestMove);
      if (bestMove !== null && bestMove >= 0 && bestMove < 9) {
        newBoard[bestMove] = 'O'; // IA joue 'O'
        setBoard(newBoard);
        setXIsNext(true);
        const winnerCheckAfterAI = getWinner(newBoard);
        if (winnerCheckAfterAI) {
          setResult(winnerCheckAfterAI.winner);
        } else if (newBoard.every((cell) => cell)) {
          setResult('Draw');
        }
      }
    }
    console.log('Meilleur coup:', bestMove);
  };

  const renderCell = (value: string | null, idx: number) => (
    <button
      key={idx}
      onClick={() => handleClick(idx)}
      className="w-full h-full flex items-center justify-center bg-transparent border-none cursor-pointer"
      style={{ aspectRatio: '1/1', position: 'relative' }}
      aria-label={`Cell ${idx}`}
    >
      {value === 'X' && (
        <Image src="/X-player.svg" alt="X" width={100} height={100} />
      )}
      {value === 'O' && (
        <Image src="/O-player.svg" alt="O" width={100} height={100} />
      )}
    </button>
  );

  // Overlay line for the winning combination
  const renderWinningLine = () => {
    console.log(winnerObj);
    if (!winnerObj) return null;
    // Position and rotation for each line index
    const lineStyles = [
      // horizontals
      {
        bottom: '35.66%',
        left: 0,
        right: 0,
        width: '20px',
        height: '100%',
        transform: 'rotate(90deg) translateY(-65%)',
        transformOrigin: 'center',
      },
      {
        top: 0,
        left: 0,
        right: 0,
        width: '20px',
        height: '100%',
        transform: 'rotate(90deg) translateY(-65%)',
        transformOrigin: 'center',
      },
      {
        top: '33.33%',
        left: 0,
        right: 0,
        width: '20px',
        height: '100%',
        transform: 'rotate(90deg) translateY(-65%)',
        transformOrigin: 'center',
      },
      // verticals
      {
        left: '12.33%',
        top: 0,
        bottom: 0,
        width: '20px',
        height: '100%',
        transform: 'none',
        transformOrigin: 'center',
      },
      {
        left: '45.99%',
        top: 0,
        bottom: 0,
        width: '20px',
        height: '100%',
        transform: 'none',
        transformOrigin: 'center',
      },
      {
        left: '81.33%',
        top: 0,
        bottom: 0,
        width: '20px',
        height: '100%',
        transform: 'none',
        transformOrigin: 'center',
      },
      // diagonals
      {
        left: 0,
        top: '-45px',
        width: '100%',
        height: '125%',
        transform: 'rotate(-51deg)',
        transformOrigin: 'center',
      },
      {
        left: 0,
        top: '-45px',
        width: '100%',
        height: '125%',
        transform: 'rotate(51deg)',
        transformOrigin: 'center',
      },
    ];
    const style = {
      position: 'absolute' as const,
      pointerEvents: 'none' as const,
      zIndex: 10,
      ...lineStyles[winnerObj.lineIndex],
    };
    return (
      <Image
        src="/green-line.svg"
        alt="Ligne gagnante"
        fill={false}
        width={style.width === '100%' ? 480 : 20}
        height={style.height === '100%' ? 352 : 20}
        style={style}
      />
    );
  };

  return (
    <div
      className="flex flex-col items-center gap-4"
      style={{ position: 'relative' }}
    >
      <div
        className="grid grid-cols-3 grid-rows-3 gap-4 w-[480px] h-[352px] bg-grid overflow-visible"
        style={{ placeItems: 'center', position: 'relative' }}
      >
        {board.map((cell, idx) => renderCell(cell, idx))}
        {renderWinningLine()}
      </div>
      <div className="flex items-center gap-4 mt-4">
        <div className="text-xl font-bold">
          {result
            ? result === 'Draw'
              ? 'Match Nul!'
              : `Gagnant: ${result}`
            : `Tour: ${xIsNext ? 'X' : 'O'}`}
        </div>
        <button
          className="ml-2 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition disabled:opacity-50"
          onClick={() => {
            setBoard(initialBoard);
            setXIsNext(true);
            setResult(null);
          }}
          disabled={!result}
        >
          {result ? 'Nouvelle Partie' : '...en cours'}
        </button>
      </div>
    </div>
  );
};

export default Grid;
