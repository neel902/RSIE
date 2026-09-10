# Note: this is vibe coded (dont sue me i dont know how to use prompt_toolkit i might fix it when i learn)



from prompt_toolkit.application import Application # type: ignore
from prompt_toolkit.buffer import Buffer # type: ignore
from prompt_toolkit.key_binding import KeyBindings # type: ignore
from prompt_toolkit.layout.containers import HSplit, Window # type: ignore
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl # type: ignore
from prompt_toolkit.layout.layout import Layout # type: ignore
from prompt_toolkit.lexers import PygmentsLexer # type: ignore
from pygments.lexers import TextLexer # type: ignore
from pygments.lexers import get_lexer_by_name # type: ignore

def create_editor_app(initial_text="", file_name="unnamed.txt"):
    # 1. Create the main text buffer and load default text
    text_buffer = Buffer(multiline=True)
    text_buffer.text = initial_text
    text_buffer.filename = file_name

    # 2. Define Key Bindings (e.g., Ctrl+Q to exit)
    kb = KeyBindings()

    @kb.add("c-q")
    def exit_(event):
        """Press Ctrl+Q to close the editor and return the text."""
        event.app.exit(result=text_buffer.text)
    try:
        usedLexer = get_lexer_by_name(text_buffer.filename.split(".")[-1] if len(text_buffer.filename.split("."))>0 else "txt").__class__ #next((val for key, val in lexers.items() if text_buffer.filename.endswith(key)), TextLexer)
    except:
        usedLexer = TextLexer

    editor_window = Window(content=BufferControl(buffer=text_buffer, lexer=PygmentsLexer(usedLexer)))

    # A simple status bar at the bottom
    def get_status_text():
        # Dynamically tracks cursor row and column
        row = text_buffer.document.cursor_position_row + 1
        col = text_buffer.document.cursor_position_col + 1
        file_name = text_buffer.filename
        return f" [Ctrl+Q] Save & Exit | {file_name} | Line: {row}, Col: {col} "

    status_bar = Window(
        content=FormattedTextControl(get_status_text),
        height=1,
        style="bg:#87CEEB #000000",  # Dark grey background with white text
    )

    # Combine the editing window and status bar vertically
    root_container = HSplit([editor_window, status_bar])

    # 4. Initialize the Application
    app = Application(
        layout=Layout(root_container, focused_element=editor_window),
        key_bindings=kb,
        full_screen=True,  # Takes over the whole terminal screen like Vim/Nano
    )

    return app


# Example Usage:
if __name__ == "__main__":
    default_content = (
        "Welcome to your custom terminal editor!\n"
        "This text is fully editable.\n"
        "You can use arrow keys, Backspace, and Enter naturally.\n"
        "Modify this text and press Ctrl+Q when you are finished."
    )

    # Launch the editor app
    app = create_editor_app(initial_text=default_content)
    final_text = app.run()  # Execution pauses here until app.exit() is triggered

    print("\n--- Editor Closed. Final Saved Content: ---")
    print(final_text)
