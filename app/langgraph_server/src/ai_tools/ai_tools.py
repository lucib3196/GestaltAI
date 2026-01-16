from pathlib import Path
from langchain.tools import tool
from app.core.settings import get_settings


output = get_settings().output_path
OUTPUT_DIR = Path(output).resolve()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@tool
def save_file(filename: str, content: str) -> str:
    """
    Save text content to a file in the application's output directory.

    This tool is intended for use by an LLM to persist generated text
    (e.g., reports, code, summaries, or data files) to disk so the file
    can later be listed and downloaded by the user via the Streamlit UI.

    The file is written using UTF-8 encoding and will overwrite any
    existing file with the same name.

    Args:
        filename (str):
            Name of the file to create (including extension), relative
            to the application's output directory (e.g., "report.txt",
            "solution.md", "data.json").

        content (str):
            The text content to write into the file.

    Returns:
        str:
            The filesystem path to the saved file as a string.
    """
    path = OUTPUT_DIR / filename
    path.write_text(content)
    return str(path)


if __name__ == "__main__":
    print(OUTPUT_DIR)
    # save_file("content.html", "hellWorld")
