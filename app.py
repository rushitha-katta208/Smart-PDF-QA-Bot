import gradio as gr
from src.backend import get_answer, load_pdf


# --- CHAT FUNCTION (STATE SAFE) ---
def chat_with_pdf(question, history):
    if not question:
        return history, ""

    answer = get_answer(question)

    history = history + [(question, answer)]
    return history, ""


# --- UPLOAD FUNCTION ---
def upload_pdf(file):
    if file is None:
        return "Please upload a PDF."

    load_pdf(file.name)
    return "✅ PDF uploaded and processed successfully!"


# --- UI ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown("""
    # 📄 Smart PDF QA Chatbot  
    ### Ask Questions, Get Instant Answers 😊  
    Upload a PDF and interact with it using AI.
    """)

    with gr.Row():
        with gr.Column(scale=1):
            pdf_file = gr.File(label="📂 Upload PDF", file_types=[".pdf"])
            upload_btn = gr.Button("Process PDF")
            upload_status = gr.Textbox(label="Status", interactive=False)

        with gr.Column(scale=2):
            chatbot = gr.Chatbot(height=400)

            msg = gr.Textbox(
                placeholder="Ask something about your PDF...",
                lines=2
            )

            send_btn = gr.Button("Send")

            state = gr.State([])  # ✅ FIX: proper chat memory

    # Upload action
    upload_btn.click(
        fn=upload_pdf,
        inputs=pdf_file,
        outputs=upload_status
    )

    # Chat action
    send_btn.click(
        fn=chat_with_pdf,
        inputs=[msg, state],
        outputs=[chatbot, msg]
    ).then(
        lambda h: h,
        inputs=state,
        outputs=state
    )


if __name__ == "__main__":
    demo.launch()
