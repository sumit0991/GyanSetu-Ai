import React, { useState, useEffect, useRef } from 'react';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

// Define shapes for data safety
interface Flashcard {
  question: string;
  answer: string;
}

interface Video {
  title: string;
  url: string;
}

interface GenerateResponse {
  answer: string;
  flashcards: Flashcard[];
  video: Video[];
  sources?: string[];
}

const MainApp: React.FC = () => {
  const [subjectName, setSubjectName] = useState<string>("");
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [topics, setTopics] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [notes, setNotes] = useState<string>("");
  const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
  const [videos, setVideos] = useState<Video[]>([]);
  const [sources, setSources] = useState<string[]>([]);
  const [activeTab, setActiveTab] = useState<'notes' | 'cards' | 'videos' | 'verify'>('notes');
  const [isDarkMode, setIsDarkMode] = useState<boolean>(localStorage.getItem('theme') === 'dark');

  const contentRef = useRef<HTMLDivElement>(null);

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

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) setSelectedFiles(Array.from(e.target.files));
  };

  const downloadPDF = async () => {
    if (!contentRef.current) return;
    setLoading(true);
    const element = contentRef.current;
    const canvas = await html2canvas(element, { scale: 2, useCORS: true, logging: false });
    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF('p', 'mm', 'a4');
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = pdf.internal.pageSize.getHeight();
    const imgWidth = pdfWidth;
    const imgHeight = (canvas.height * pdfWidth) / canvas.width;
    let heightLeft = imgHeight;
    let position = 0;
    pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
    heightLeft -= pdfHeight;
    while (heightLeft > 0) {
      position = heightLeft - imgHeight;
      pdf.addPage();
      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
      heightLeft -= pdfHeight;
    }
    const fileName = `${topics.replace(/\s+/g, '_').toLowerCase()}_notes.pdf`;
    pdf.save(fileName);
    setLoading(false);
  };

  const askAI = async () => {
    if (!subjectName.trim() || selectedFiles.length === 0 || !topics.trim()) {
      return alert("Please fill in all fields.");
    }
    setLoading(true);
    const formData = new FormData();
    formData.append("subject", subjectName);
    formData.append("topics", topics);
    selectedFiles.forEach((file) => formData.append("files", file));
    try {
      const response = await fetch('http://127.0.0.1:8000/generate-notes', { method: 'POST', body: formData });
      const data: GenerateResponse = await response.json();
      setNotes(data.answer);
      setFlashcards(data.flashcards || []);
      setVideos(data.video || []);
      setSources(data.sources || []);
      setActiveTab('notes');
    } catch (error) {
      alert("Error: " + (error as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col lg:flex-row w-screen min-h-screen bg-slate-50 dark:bg-slate-950 transition-colors duration-300">

      {/* Sidebar Control Panel */}
      <div className="lg:w-[450px] bg-white dark:bg-slate-900 p-8 border-r border-slate-200 dark:border-slate-800 shadow-xl no-print flex flex-col pt-24 shrink-0">
        <div className="space-y-8 flex-grow">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-6 uppercase tracking-tight">Content Creator</h2>

          <div className="space-y-2">
            <label className="block text-xs font-black text-slate-500 dark:text-slate-400 uppercase tracking-widest ml-1">Subject Name</label>
            <input type="text" placeholder="e.g. Thermodynamics" className="w-full border-2 border-slate-100 dark:border-slate-800 p-4 rounded-2xl bg-slate-50 dark:bg-slate-800 dark:text-white outline-none focus:border-blue-500 transition-all" value={subjectName} onChange={(e) => setSubjectName(e.target.value)} />
          </div>

          <div className="space-y-2">
            <label className="block text-xs font-black text-slate-500 dark:text-slate-400 uppercase tracking-widest ml-1">Upload Sources (PDF)</label>
            <input type="file" multiple accept=".pdf" className="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 dark:file:bg-slate-800 dark:file:text-slate-300" onChange={handleFileChange} />
          </div>

          <div className="space-y-2">
            <label className="block text-xs font-black text-slate-500 dark:text-slate-400 uppercase tracking-widest ml-1">Topics</label>
            <textarea rows={8} placeholder="Enter topics..." className="w-full border-2 border-slate-100 dark:border-slate-800 p-4 rounded-2xl bg-slate-50 dark:bg-slate-800 dark:text-white outline-none resize-none focus:border-blue-500 transition-all" value={topics} onChange={(e) => setTopics(e.target.value)}></textarea>
          </div>

          <button onClick={askAI} disabled={loading} className="w-full py-5 bg-blue-600 hover:bg-blue-700 text-white rounded-2xl font-black text-lg shadow-lg shadow-blue-500/30 transition-all transform active:scale-95">
            {loading ? "Processing..." : "Generate Content"}
          </button>
        </div>
      </div>

      {/* Main Content Area - This area scrolls */}
      <div className="flex-1 p-6 md:p-12 overflow-y-auto pt-24 h-screen scroll-smooth">
        {!notes ? (
          <div className="h-full flex items-center justify-center border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-[3rem]">
            <div className="text-center space-y-4">
              <div className="text-6xl">📖</div>
              <p className="text-slate-400 dark:text-slate-600 font-medium italic">Upload books to generate exhaustive notes.</p>
            </div>
          </div>
        ) : (
          <div className="mx-auto max-w-[1100px] space-y-6 animate-in fade-in duration-700">
            <div className="bg-white dark:bg-slate-900 shadow-2xl rounded-[2.5rem] border border-slate-200 dark:border-slate-800 overflow-hidden relative">

              {/* THE ONLY WORKING BUTTONS - STICKY UNDER "COMPREHENSIVE LEARNING MATERIAL" */}
              <div className="sticky top-0 z-50 bg-white dark:bg-slate-900 p-8 pb-6 border-b border-slate-100 dark:border-slate-800 no-print">
                <div className="flex items-center gap-4 mb-6">
                    <div className="h-[2px] flex-1 bg-slate-100 dark:bg-slate-800"></div>
                    <h3 className="text-[10px] font-black text-slate-400 dark:text-slate-500 uppercase tracking-[0.2em] whitespace-nowrap">
                        Comprehensive Learning Material
                    </h3>
                    <div className="h-[2px] flex-1 bg-slate-100 dark:bg-slate-800"></div>
                </div>

                {/* These are the stylized buttons you need */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {[
                    { id: 'notes', label: 'Notes', icon: '📄' },
                    //{ id: 'cards', label: 'Flashcards', icon: '🧠' },
                    //{ id: 'videos', label: 'Videos', icon: '📽️' },
                    //{ id: 'verify', label: 'Verify', icon: '🔍' }
                  ].map((btn) => (
                    <button
                      key={btn.id}
                      onClick={() => setActiveTab(btn.id as any)}
                      className={`flex items-center justify-center gap-2 py-4 px-2 rounded-xl font-bold text-sm uppercase transition-all border-2
                        ${activeTab === btn.id
                          ? 'bg-blue-600 border-blue-600 text-white shadow-lg shadow-blue-500/30'
                          : 'bg-transparent border-slate-200 dark:border-slate-800 text-slate-500 hover:border-blue-400'}`}
                    >
                      <span className="text-base">{btn.icon}</span>
                      {btn.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Content Area */}
              <div ref={contentRef} className="p-10 min-h-[700px]">
                {activeTab === 'notes' && (
                  <div className="prose dark:prose-invert max-w-none text-slate-800 dark:text-slate-200" dangerouslySetInnerHTML={{ __html: notes }} />
                )}

                {activeTab === 'cards' && (
                  <div className="grid gap-6">
                    <h2 className="text-xl font-black text-slate-900 dark:text-white uppercase tracking-tight mb-4">Active Recall Flashcards</h2>
                    {flashcards.map((card, idx) => (
                      <div key={idx} className="p-8 border-l-8 border-blue-600 bg-blue-50/30 dark:bg-slate-800/50 rounded-3xl shadow-sm">
                        <p className="font-black text-blue-600 uppercase text-[10px] mb-2 tracking-widest">Question</p>
                        <p className="text-xl font-bold text-slate-900 dark:text-white mb-6">{card.question}</p>
                        <hr className="border-slate-200 dark:border-slate-700 mb-6" />
                        <p className="font-black text-slate-400 uppercase text-[10px] mb-2 tracking-widest">Answer</p>
                        <p className="text-lg text-slate-700 dark:text-slate-300 leading-relaxed">{card.answer}</p>
                      </div>
                    ))}
                  </div>
                )}

                {activeTab === 'videos' && (
                  <div className="space-y-12">
                    {videos.map((v, idx) => (
                      <div key={idx} className="w-full">
                        <h3 className="text-2xl font-black mb-6 text-slate-900 dark:text-white border-b pb-2 border-slate-100 dark:border-slate-800">{v.title}</h3>
                        <div className="relative aspect-video rounded-[2rem] overflow-hidden shadow-2xl no-print">
                          <iframe className="absolute inset-0 w-full h-full" src={v.url.replace("watch?v=", "embed/")} title={v.title} allowFullScreen></iframe>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {activeTab === 'verify' && (
                  <div className="space-y-6">
                    <div className="p-6 bg-blue-600 text-white rounded-[2rem] shadow-xl shadow-blue-500/20">
                        <h4 className="font-black uppercase tracking-widest text-sm">RAG Verification System</h4>
                        <p className="text-blue-100 mt-2 text-sm leading-relaxed">Evidence retrieved from source PDFs.</p>
                    </div>
                    {sources.length > 0 ? sources.map((src, idx) => (
                      <div key={idx} className="p-6 bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800 rounded-3xl text-sm font-mono text-slate-600 dark:text-slate-400 italic">
                        "{src}"
                      </div>
                    )) : <p className="text-center py-20 text-slate-300">No source evidence available.</p>}
                  </div>
                )}
              </div>
            </div>

            <button onClick={downloadPDF} disabled={loading} className="w-full py-5 bg-slate-900 dark:bg-blue-600 text-white rounded-2xl font-black hover:opacity-90 transition-all no-print shadow-xl">
              {loading ? "Processing..." : `📥 Download Content as PDF`}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default MainApp;
