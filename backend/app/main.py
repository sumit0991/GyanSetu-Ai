import os
import shutil
import re
from typing import List
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from backend.app.schemas import QueryResponse
from backend.app.services.orchestrator import CourseOrchestrator
from backend.app.services.image_service import ImageService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a local storage path for user uploads
UPLOAD_DIR = "backend/data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def read_root():
    return {"status": "Online", "message": "Mini2 Intelligent-Notes Engine is running"}


@app.post("/generate-notes", response_model=QueryResponse)
async def generate_notes(
        subject: str = Form(...),
        topics: str = Form(...),
        files: List[UploadFile] = File(...)
):
    try:
        # 1. RISK-FREE FILE MANAGEMENT
        subject_folder = os.path.join(UPLOAD_DIR, subject.replace(" ", "_"))
        os.makedirs(subject_folder, exist_ok=True)

        saved_file_paths = []
        for file in files:
            file_path = os.path.join(subject_folder, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            saved_file_paths.append(file_path)

        # 2. INITIALIZE ORCHESTRATOR
        bot = CourseOrchestrator(subject)
        topics_list = [t.strip() for t in topics.split('-') if t.strip()]

        if not topics_list:
            raise HTTPException(status_code=400, detail="No topics found in input.")

        all_topic_notes = []
        all_topic_videos = []
        all_flashcards_html = []
        raw_context_snippets = []  # New list to store verification chunks

        for t in topics_list:
            # The orchestrator uses the uploaded PDFs to generate the content
            result_package = bot.generate(t)
            topic_result = result_package["answer"]

            # --- NEW LOGIC: EXTRACT RAW CONTEXT FOR VERIFICATION ---
            # Most RAG orchestrators return the retrieved chunks in a 'context' or 'source_documents' key
            if "context" in result_package:
                raw_context_snippets.append(result_package["context"])

            # --- PRESERVED LOGIC: MARKDOWN TO HTML BOLDING ---
            topic_result = topic_result.replace("**", "<b>")
            topic_result = re.sub(r'<b>\s*([^<]+?)\s*<b>', r'<b class="text-blue-700 dark:text-blue-400">\1</b>',
                                  topic_result)

            video_data = result_package.get("video")
            flashcards = result_package.get("flashcards", [])

            # --- PRESERVED LOGIC: VIDEO HTML ---
            if video_data:
                video_html = f"""
                <div class="video-section-item" style="margin-bottom: 50px; width: 100%;">
                    <h3 class="text-blue-800 dark:text-blue-400" style="font-size: 20px; font-weight: bold; margin-bottom: 20px;">Video Tutorial: {t.upper()}</h3>
                    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; background: #000; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
                        <iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" 
                                src="{video_data['url']}" frameborder="0" allowfullscreen></iframe>
                    </div>
                    <p class="text-slate-500 dark:text-slate-400" style="margin-top: 15px; font-style: italic;">{video_data['title']}</p>
                </div>
                """
                all_topic_videos.append(video_html)

            # --- PRESERVED LOGIC: DIAGRAM FETCHING ---
            image_data = ImageService.get_exam_diagram(t)
            image_html = ""
            if image_data:
                secure_url = image_data['url'].replace("http://", "https://")
                image_html = f"""
                <div class="image-container bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600" style="margin: 30px 0; text-align: center; padding: 20px; border-radius: 12px;">
                    <p style="font-size: 10px; font-weight: 800; color: #3b82f6; text-transform: uppercase; margin-bottom: 12px;">Technical Reference Diagram</p>
                    <img src="{secure_url}" style="max-width: 100%; height: auto; border-radius: 6px;">
                    <p class="text-slate-500 dark:text-slate-400" style="font-size: 10px; margin-top: 12px;">Fig: {image_data['title']}</p>
                </div>
                """

            if "<b>3." in topic_result:
                topic_result = topic_result.replace("<b>3.", f"{image_html}<b>3.")
            else:
                topic_result += f"\n\n{image_html}"

            # --- PRESERVED LOGIC: FINAL SECTION WRAPPING ---
            formatted_section = f"""
            <h2 class="text-blue-800 dark:text-blue-400 border-blue-600 dark:border-blue-500" style='font-weight: bold; border-bottom: 3px solid; padding-bottom: 5px; margin-top: 20px; margin-bottom: 10px; text-transform: uppercase; font-size: 1.25rem;'>TOPIC: {t.upper()}</h2>
            <div class="topic-body text-slate-700 dark:text-slate-300" style="line-height: 1.6; white-space: pre-wrap; text-align: left;">{topic_result}</div>
            <hr class="border-slate-200 dark:border-slate-700" style='border: 0; border-top: 1px solid; margin: 25px 0;'>
            """
            all_topic_notes.append(formatted_section)

            # --- PRESERVED LOGIC: FLASHCARDS ---
            if flashcards:
                for card in flashcards:
                    card_html = f"""
                    <div class="flashcard-item bg-slate-50 dark:bg-slate-700/50 border-slate-200 dark:border-slate-600" style="border: 2px solid; border-radius: 12px; padding: 20px; margin-bottom: 15px;">
                        <p class="text-blue-700 dark:text-blue-400" style="font-weight: 800; margin-bottom: 10px;">QUESTION:</p>
                        <p class="text-slate-700 dark:text-slate-200" style="margin-bottom: 15px; font-weight: 500;">{card['question']}</p>
                        <details style="cursor: pointer;">
                            <summary class="text-blue-600 dark:text-blue-400" style="font-weight: bold; font-size: 14px; outline: none;">VIEW ANSWER</summary>
                            <p class="bg-white dark:bg-slate-800 text-emerald-700 dark:text-emerald-400 border-emerald-500" style="margin-top: 10px; padding: 15px; border-left: 4px solid; border-radius: 4px;">{card['answer']}</p>
                        </details>
                    </div>
                    """
                    all_flashcards_html.append(card_html)

        # --- PRESERVED LOGIC: UI ASSEMBLY ---
        final_ui_html = f"""
        <div class="border-slate-200 dark:border-slate-700" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid; padding-bottom: 10px;">
            <span style="font-size: 12px; font-weight: bold; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Comprehensive Learning Material</span>
        </div>

        <div class="tab-controls no-print" style="display: flex; gap: 10px; margin-bottom: 30px;">
            <button onclick="showTab('notes')" id="tab-btn-notes" class="bg-blue-800 text-white" style="flex: 1; padding: 12px; border-radius: 8px; border: none; font-weight: bold; cursor: pointer;">📄 NOTES</button>
            <button onclick="showTab('flashcards')" id="tab-btn-flashcards" class="bg-white dark:bg-slate-800 text-slate-500 dark:text-slate-400 border-slate-200 dark:border-slate-700" style="flex: 1; padding: 12px; border-radius: 8px; border: 2px solid; font-weight: bold; cursor: pointer;">🧠 FLASHCARDS</button>
            <button onclick="showTab('videos')" id="tab-btn-videos" class="bg-white dark:bg-slate-800 text-slate-500 dark:text-slate-400 border-slate-200 dark:border-slate-700" style="flex: 1; padding: 12px; border-radius: 8px; border: 2px solid; font-weight: bold; cursor: pointer;">🎥 VIDEOS</button>
            <button onclick="showTab('verify')" id="tab-btn-verify" class="bg-white dark:bg-slate-800 text-slate-500 dark:text-slate-400 border-slate-200 dark:border-slate-700" style="flex: 1; padding: 12px; border-radius: 8px; border: 2px solid; font-weight: bold; cursor: pointer;">🔍 VERIFY</button>
        </div>

        <div id="notes-view" class="tab-content" style="display: block; width: 100%;">
            {"".join(all_topic_notes)}
        </div>

        <div id="flashcards-view" class="tab-content" style="display: none; width: 100%;">
            <h2 class="text-blue-800 dark:text-blue-400" style="font-weight: bold; margin-bottom: 20px; text-transform: uppercase;">Active Recall Flashcards</h2>
            {"".join(all_flashcards_html) if all_flashcards_html else "<p class='dark:text-slate-400'>Generating cards...</p>"}
        </div>

        <div id="videos-view" class="tab-content" style="display: none; width: 100%;">
            {"".join(all_topic_videos) if all_topic_videos else "<p style='text-align:center; padding:50px;' class='text-slate-500 dark:text-slate-400'>No videos found for these topics.</p>"}
        </div>

        <div id="verify-view" class="tab-content" style="display: none; width: 100%;">
            <h2 class="text-blue-800 dark:text-blue-400" style="font-weight: bold; margin-bottom: 10px; text-transform: uppercase;">RAG Source Verification</h2>
            <p style="font-size: 13px; margin-bottom: 20px;" class="text-slate-500">The following snippets were extracted from your uploaded files and provided to Gemini as context:</p>
            {"".join([f'<div style="padding:15px; margin-bottom:10px; font-size:12px; font-family:monospace; border-radius:8px;" class="bg-slate-100 dark:bg-slate-900 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700 italic">"...{s}..."</div>' for s in raw_context_snippets])}
        </div>

        <script>
            function showTab(tabId) {{
                document.querySelectorAll('.tab-content').forEach(t => t.style.display = 'none');
                document.querySelectorAll('.tab-controls button').forEach(b => {{
                    b.className = "bg-white dark:bg-slate-800 text-slate-500 dark:text-slate-400 border-slate-200 dark:border-slate-700";
                    b.style.backgroundColor = "";
                    b.style.color = "";
                }});

                document.getElementById(tabId + '-view').style.display = 'block';
                const activeBtn = document.getElementById('tab-btn-' + tabId);
                activeBtn.className = "bg-blue-800 text-white";
                activeBtn.style.backgroundColor = "#1e40af";
                activeBtn.style.color = "white";
            }}
        </script>
        """

        # Return response matching the plural 'topics' if needed in the schema
        # Note: Added 'sources' if your QueryResponse schema supports it,
        # otherwise it's baked into the final_ui_html above.
        return QueryResponse(topic=topics, answer=final_ui_html)

    except Exception as e:
        print(f"System Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))