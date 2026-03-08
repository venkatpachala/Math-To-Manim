"""
Pipeline test for gradient descent.

Test Validates:
- PrerequisiteExplorer which finds the relevant prerequistics
- MathematicalContentEnricher which enriches the content with equations, definitions, interpretations, and examples
- VisualDesigner creates visual representations of the concepts
- NarrativeComposer writes a 500+ Word scripts
"""
import asyncio
import json
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent 
sys.path.insert(0, str(project_root))

#load .env file
from dotenv import load_dotenv
load_dotenv()

#Import the main orchestrator - this runs the whole pipeline
from swarm.orchestrator import SwarmOrchestrator

async def test_gradient_descent_pipeline():
    """End to end pipeline test for gradient descent."""

    #setup
    topic="Gradient Descent"

    print("\n" + "="*70)
    print(f"PIPELINE TEST: {topic}")
    print("="*70)

    #Run the Pipeline
    print("\nRunning the pipeline...")
    orchestrator= SwarmOrchestrator(topic)

    print(f" Running the pipeline... {topic}")
    print(" This may take a few minutes as it involves multiple steps and API calls.")
    print()

    result= await orchestrator.process_async(topic)

    #CHECK 1: Tree is built
    assert result.enriched_tree is not None, \
    "FAIL"

    print(f" CHECK 1 PASSED: Tree built")
    print(f"Root concept")
    print(f" - {result.enriched_tree.concept}")


    #CHECK 2: Finding prerequisties

    prereqs= result.enriched_tree.prerequisites
    assert len(prereqs) > 0, "FAIL: No prerequisties found"

    print(f" CHECK 2 PASSED: Prerequisites found")
    for p in prereqs:
        indent = "   " * (p.depth)
        print(f" {indent}- {p.concept} (Depth: {p.depth})")

    #CHECK 3: Equation added by MathematicalEnrichmer

    equations= result.enriched_tree.content.equations
    assert len(equations) > 0, "FAIL: No equations added by MathematicalContentEnricher"

    print(f" CHECK 3 PASSED: Equations added by MathematicalContentEnricher")
    for eq in equations:
        print(f" - {eq[:70]}")

    #CHECK 4: Visuals created by VisualDesigner
    visuals= result.enriched_tree.visuals_spec
    assert visuals is not None and len(visuals) > 0, "FAIL: No visuals created by VisualDesigner"

    print(f" CHECK 4 PASSED: Visuals created by VisualDesigner")
    print(f" Keys: {list(visuals.keys())}")

    #CHECK 5: Narrative script created by NarrativeComposer

    narrative= result.narrative_prompt or ""
    assert len(narrative) > 500, "FAIL: Narrative script is too short or not created by NarrativeComposer"
    print(f" CHECK 5 PASSED: Narrative script created by NarrativeComposer")
    print(f" Narrative script length: {len(narrative)} characters")

    print()
    if result.error:
        print(f"Pipeline completed with errors: {result.error}")
    else:
        print("Pipeline completed successfully without errors.")

    
    #Saving the output in output folder
    output_dir=Path("examples/outputs")
    output_dir.mkdir(exist_ok=True)

    tree_summary={
        "topic": topic,
        "root_concept": result.enriched_tree.concept,
        "prereuisties": [p.concept for p in prereqs],
        "equations": equations,
        "visual_spec_keys": list(visuals.keys()),
        "narrative_length": len(narrative),
        "error": result.error,
        "equations_count": len(equations)

    }

    treepath= output_dir 
    with open(treepath, "w", encoding="utf-8") as f:
        json.dump(tree_summary, f, indent=2)
    
    narrative_path= output_dir 
    narrative_path.write_text(narrative, encoding="utf-8")

    print("tree summary and narrative script saved in examples/outputs {tree_path} and {narrative_path}")

    return result
    
if __name__ == "__main__":
    try:
        asyncio.run(test_gradient_descent_pipeline())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
