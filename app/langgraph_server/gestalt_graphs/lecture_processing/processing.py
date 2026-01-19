from .graph import graph as lecture_graph, State as LectureState
from pathlib import Path
import asyncio
from langgraph_server.gestalt_graphs.utils import to_serializable
import json

import asyncio
import json
from pathlib import Path


async def process_single_lecture(
    pdf_path: Path,
    save_root: Path,
):
    """
    Run the lecture graph for a single PDF and save the output.
    """
    filename = pdf_path.name
    graph_input = LectureState(lecture_pdf=pdf_path)

    try:
        response = await lecture_graph.ainvoke(graph_input)

        print(f"\n--- Graph Response ({filename}) ---")
        print(response)

        # Create output directory
        output_dir = save_root / filename
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save JSON output (UTF-8 safe)
        data_path = output_dir / "output.json"
        data_path.write_text(
            json.dumps(to_serializable(response), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    except Exception as e:
        print(f"\n❌ Error while processing {filename}:")
        print(e)


async def main():
    folder_path = Path(r"langgraph_server\data\TransportLecture").resolve()
    output_path = Path(
        r"langgraph_server/gestalt_graphs/lecture_processing/transport_lecture"
    ).resolve()

    tasks = [
        process_single_lecture(p, output_path)
        for p in folder_path.iterdir()
        if p.is_file() and p.suffix.lower() == ".pdf"
    ]

    if not tasks:
        print("⚠️ No PDF files found.")
        return

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
