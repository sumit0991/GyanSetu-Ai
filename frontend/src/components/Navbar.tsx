import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [isDarkMode, setIsDarkMode] = useState(() => {
    return localStorage.getItem('theme') === 'dark' ||
           (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches);
  });

  useEffect(() => {
    const root = window.document.documentElement;
    if (isDarkMode) {
      root.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      root.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [isDarkMode]);

  // Don't show the full navbar on the actual /app route if you want to keep your original sidebar clean
  const isAppPath = location.pathname === '/app';

  return (
    <nav className="fixed top-0 left-0 w-full z-50 flex justify-between items-center px-8 py-4 bg-transparent backdrop-blur-md">
      {/* Clickable Logo to return Home */}
      <div
          onClick={() => navigate('/')}
          className="cursor-pointer hover:opacity-80 transition-opacity"
        >

          <h1 className="relative text-2xl md:text-3xl font-black
          text-blue-600 dark:text-blue-400 tracking-tight flex items-center">

            Gyaan

            {/* SETU Bridge */}
            <span className="relative inline-block mx-1">
              Setu

              <svg
                className="absolute left-0 top-[75%] w-full h-4"
                viewBox="0 0 300 60"
                preserveAspectRatio="none"
              >

                <defs>
                  <linearGradient id="navBridgeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#ef4444" />
                    <stop offset="100%" stopColor="#f97316" />
                  </linearGradient>
                </defs>

                <path
                  d="M10 40 Q150 10 290 40"
                  stroke="url(#navBridgeGradient)"
                  strokeWidth="10"
                  fill="none"
                  strokeLinecap="round"
                />
              </svg>
            </span>

            {/* AI */}
            <span className="ml-2 relative inline-block">
              A
              <span className="relative inline-block">
                I

                {/* AI Node */}
                <span className="absolute -top-2 left-1/2
                -translate-x-1/2 w-3 h-3
                bg-red-500 rounded-full"></span>

              </span>
            </span>

          </h1>

      </div>

      <div className="flex items-center gap-6">
        {!isAppPath && (
          <button
            onClick={() => navigate('/pricing')}
            className="text-sm font-bold text-slate-600 dark:text-slate-300 hover:text-blue-600 transition-colors"
          >
            Pricing
          </button>
        )}

        {/* Professional Toggle Button */}
        <button
          onClick={() => setIsDarkMode(!isDarkMode)}
          className="p-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm hover:shadow-md transition-all flex items-center justify-center group"
          aria-label="Toggle Theme"
        >
          {isDarkMode ? (
            <span className="text-yellow-400 text-xl group-hover:rotate-12 transition-transform">☀️</span>
          ) : (
            <span className="text-blue-600 text-xl group-hover:-rotate-12 transition-transform">🌙</span>
          )}
        </button>
      </div>
    </nav>
  );
};

export default Navbar;