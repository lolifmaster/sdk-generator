import gradio as gr


def alternatively_agree(message, history):
    if len(history) % 2 == 0:
        return f"Yes, I do think that '{message}'"
    else:
        return "I don't think so"


gr.ChatInterface(alternatively_agree).launch(share=True)
