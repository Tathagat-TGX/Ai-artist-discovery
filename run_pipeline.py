from agents.discovery_agent import run_discovery
from agents.intelligence_agent import run_intelligence
from agents.outreach_agent import run_outreach


def run_pipeline():

    print("Starting AI Artist Discovery System")

    run_discovery()
    run_intelligence()
    run_outreach()

    print("Pipeline completed")


if __name__ == "__main__":
    run_pipeline()