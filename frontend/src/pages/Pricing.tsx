import React from 'react';
import { useNavigate } from 'react-router-dom';

const Pricing: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="w-screen min-h-screen bg-slate-50 dark:bg-slate-950 flex flex-col items-center justify-center py-16 px-4 md:px-10 overflow-x-hidden">

      {/* Header Section - Explicitly set text-slate-900 for light mode visibility */}
      <div className="w-full max-w-7xl text-center mb-16 md:mb-24 space-y-4">
        <h2 className="text-5xl md:text-7xl font-black text-slate-900 dark:text-white tracking-tight leading-tight">
          Choose Your <span className="text-blue-600">Learning Speed</span>
        </h2>
        <p className="text-xl md:text-2xl text-slate-600 dark:text-slate-400 font-medium">
          Start for free and upgrade as you grow.
        </p>
      </div>

      <div className="w-full max-w-7xl flex flex-col lg:flex-row gap-10 justify-center items-center lg:items-stretch">

        {/* --- FREE PLAN CARD --- */}
        <div className="w-full max-w-md bg-white dark:bg-slate-900 p-10 md:p-14 rounded-[3rem] border border-slate-200 dark:border-slate-800 flex flex-col shadow-sm hover:shadow-xl transition-all">
          <h3 className="text-3xl font-bold text-slate-900 dark:text-white mb-2">Standard Access</h3>
          <p className="text-slate-500 mb-8 font-medium italic">Perfect for individual subjects.</p>

          {/* Price - Ensure dark text */}
          <div className="text-6xl font-black text-slate-900 dark:text-white mb-10">
            $0<span className="text-xl text-slate-400 font-normal">/mo</span>
          </div>

          <ul className="space-y-5 mb-12 text-left flex-grow">
            {/* Added text-slate-700 for better contrast on white background */}
            <li className="flex items-center gap-3 text-lg text-slate-700 dark:text-slate-300">
              <span className="text-green-500 font-bold text-xl">✓</span> RAG-Powered Notes
            </li>
            <li className="flex items-center gap-3 text-lg text-slate-700 dark:text-slate-300">
              <span className="text-green-500 font-bold text-xl">✓</span> 20 response/Day
            </li>
            <li className="flex items-center gap-3 text-lg text-slate-700 dark:text-slate-300">
              <span className="text-green-500 font-bold text-xl">✓</span> Basic Verification Tab
            </li>
            <li className="flex items-center gap-3 text-lg text-slate-700 dark:text-slate-300">
              <span className="text-green-500 font-bold text-xl">✓</span> PDF Export
            </li>
          </ul>

          <button
            onClick={() => navigate('/app')}
            className="w-full py-5 bg-blue-50 hover:bg-blue-600 text-blue-600 hover:text-white font-bold rounded-2xl transition-all text-xl"
          >
            Start Free
          </button>
        </div>

        {/* --- PRO PLAN CARD --- */}
        <div className="w-full max-w-md bg-white dark:bg-slate-900 p-10 md:p-14 rounded-[3rem] border-4 border-blue-600 shadow-2xl flex flex-col relative transform lg:-translate-y-8">
          <div className="absolute -top-6 left-1/2 -translate-x-1/2 bg-blue-600 text-white px-8 py-2 rounded-full text-sm font-black uppercase tracking-widest shadow-lg">
            Launching Soon
          </div>

          <h3 className="text-3xl font-bold text-slate-900 dark:text-white mb-2">Pro Access</h3>
          <p className="text-slate-500 mb-8 font-medium italic">For serious academic performance.</p>

          <div className="text-6xl font-black text-slate-900 dark:text-white mb-10">
            $5.00<span className="text-xl text-slate-400 font-normal">/mo</span>
          </div>

          <ul className="space-y-5 mb-12 text-left flex-grow">
            <li className="flex items-center gap-3 text-lg font-bold text-slate-800 dark:text-slate-200">
              <span className="text-blue-500 text-xl">⭐</span> Everything is Standard
            </li>
            <li className="flex items-center gap-3 text-lg font-bold text-slate-800 dark:text-slate-200">
              <span className="text-blue-500 text-xl">⭐</span> 150+ response/Day
            </li>
            <li className="flex items-center gap-3 text-lg font-bold text-slate-800 dark:text-slate-200">
              <span className="text-blue-500 text-xl">⭐</span> Advanced Diagram Gen
            </li>
            <li className="flex items-center gap-3 text-lg font-bold text-slate-800 dark:text-slate-200">
              <span className="text-blue-500 text-xl">⭐</span> Best for academics
            </li>
          </ul>

          <button
            onClick={() => alert("Scholar Pro is coming soon!")}
            className="w-full py-5 bg-blue-600 hover:bg-blue-700 text-white font-black rounded-2xl shadow-xl transition-all text-xl"
          >
            Purchase
          </button>
        </div>

      </div>
    </div>
  );
};

export default Pricing;