from pathlib import Path
import json
from .graph import State
import asyncio


async def postprocess_lecture_output(
    input_json_path: Path,
    output_text_path: Path,
) -> None:
    """
    Postprocess a lecture graph output JSON into a cleaned, human-readable
    text artifact.

    This function:
    - Loads the graph output JSON
    - Validates it against the State model
    - Converts structured lecture artifacts into formatted text
    - Writes the final output to a text file

    Parameters
    ----------
    input_json_path : Path
        Path to the JSON file produced by the lecture processing graph.

    output_text_path : Path
        Path where the cleaned text output should be written.
    """

    # Load and validate graph output
    content = json.loads(input_json_path.read_text(encoding="utf-8"))
    validated = State.model_validate(content)

    # Extract metadata
    lecture_pdf_name = Path(validated.lecture_pdf).name

    # Convert structured outputs to text
    lecture_analysis_text = validated.lecture_analysis.as_string()  # type: ignore

    derivations_text = "".join(d.as_string() for d in validated.derivations)

    questions_text = "".join(q.as_string() for q in validated.extracted_questions)

    # Assemble final output
    final_text = (
        f"# Lecture Source: {lecture_pdf_name}\n\n"
        f"{lecture_analysis_text}\n\n"
        f"## Derivations\n\n"
        f"{derivations_text}\n\n"
        f"## Questions\n\n"
        f"{questions_text}"
    )

    # Write output
    output_text_path.parent.mkdir(parents=True, exist_ok=True)
    output_text_path.write_text(final_text, encoding="utf-8", )


async def main():
    folder_path = Path(
        "langgraph_server/gestalt_graphs/lecture_processing/transport_lecture"
    ).resolve()

    filename = "output.json"
    tasks = []

    for p in folder_path.iterdir():
        if not p.is_dir():
            continue

        output_text_name = f"{p.name.split('.')[0]}.txt"
        output = p / output_text_name
        data = p / filename

        tasks.append(
            postprocess_lecture_output(
                data,
                output_text_path=output,
            )
        )

    # Run all postprocessing concurrently
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
