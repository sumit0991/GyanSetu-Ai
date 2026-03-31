import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="w-screen min-h-screen bg-slate-50 dark:bg-slate-900 flex flex-col items-center justify-center p-6 text-center overflow-x-hidden">
      <div className="w-full max-w-6xl space-y-12 animate-in fade-in duration-1000">
        <h1 className="relative text-7xl md:text-9xl font-black
            text-blue-700 dark:text-blue-400 tracking-tight">

              Gyaan

              {/* SETU with Bridge */}
              <span className="relative inline-block">
                Setu

                {/* Bridge */}
                <svg
                  className="absolute left-0 top-[89%] w-full h-7"
                  viewBox="0 0 300 60"
                  preserveAspectRatio="none"
                >

                  {/* Gradient Definition */}
                  <defs>
                    <linearGradient id="bridgeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#ef4444" />   {/* red */}
                      <stop offset="100%" stopColor="#f97316" /> {/* orange */}
                    </linearGradient>
                  </defs>

                  {/* Smile Bridge */}
                  <path
                    d="M10 40 Q150 10 290 40"
                    stroke="url(#bridgeGradient)"
                    strokeWidth="8"
                    strokeWidth="19"
                    fill="none"
                    strokeLinecap="round"
                  />

                </svg>
              </span>

              {/* AI with custom red dot */}
              <span className="ml-6 relative inline-block">
                A
                <span className="relative inline-block">
                  I

                  {/* Red AI Node */}
                  <span className="absolute -top-4 left-1/2
                  -translate-x-1/2 w-8 h-8
                  bg-red-500 rounded-full"></span>

                </span>
              </span>

        </h1>
        <p
          className="
            text-2xl md:text-3xl
            text-blue-300
            font-medium
            max-w-3xl mx-auto
            leading-relaxed
          "
          style={{
            textShadow:
              "0 0 6px rgba(96,165,250,0.6), 0 0 20px rgba(59,130,246,0.35)"
          }}
        >
                Bridging Knowledge and Intelligent Learning
        </p>
        <p className="text-2xl md:text-3xl text-slate-600 dark:text-slate-400 font-medium max-w-3xl mx-auto leading-relaxed">
          Best <span className="text-blue-600 font-bold">Source-Anchored</span> AI study partner.
          Verifiable notes and flashcards directly from your textbooks.
        </p>

        <div className="pt-10">
          <button
            onClick={() => navigate('/pricing')}
            className="px-16 py-6 bg-blue-600 hover:bg-blue-700 text-white text-2xl font-bold rounded-2xl shadow-[0_20px_50px_rgba(8,112,184,0.4)] transition-all transform hover:scale-105 active:scale-95"
          >
            Get Started
          </button>
        </div>

        <div className="grid md:grid-cols-3 gap-12 mt-24 pt-16 border-t border-slate-200 dark:border-slate-800">
          <div>
            <h3 className="font-bold text-xl dark:text-white mb-2">🛡️ Zero Hallucinations</h3>
            <p className="text-slate-500">Grounded strictly in your specific PDFs.</p>
          </div>
          <div>
            <h3 className="font-bold text-xl dark:text-white mb-2">🔍 Verify Source</h3>
            <p className="text-slate-500">Cross-reference every fact with raw book text.</p>
          </div>
          <div>
            <h3 className="font-bold text-xl dark:text-white mb-2">🎥 Multi-Modal</h3>
            <p className="text-slate-500">Notes, Flashcards, and Video walkthroughs.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;