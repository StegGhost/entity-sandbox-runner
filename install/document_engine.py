import os
import json

TEMPLATE_PATH = "install/templates"


def generate_document(doc_type, topic):
    base = {
        "title": topic,
        "author": "Rigel Randolph",
    }

    if doc_type == "preprint":
        return f"""# {topic}

## Abstract
This document defines {topic}.

## Core Equation
U = stability + trust + (1 - constraint pressure) + history

## Conclusion
Formal governed computation system.
"""

    if doc_type == "whitepaper":
        return f"""# {topic} Whitepaper

## Overview
System-level explanation of {topic}.

## Architecture
Governed execution model.
"""

    if doc_type == "technical_spec":
        return f"""# {topic} Specification

## Interface
## Inputs
## Outputs
## Constraints
"""

    return f"# {topic}"
