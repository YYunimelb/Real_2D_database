
# Atomic Structure Analysis for Layered Materials

## Overview
This repository focuses on the analysis of atomic structures derived from layered materials. The foundational database, `layered_materials.json`, comprises diverse layered materials. We use a series of scripts to process this data, filter out incorrect or non-essential cases, and ultimately derive 2D and 3D structures for further analysis.

## Repository Structure

### Data
- **`layered_materials.json`**: Initial database with details on various layered materials.
- **`2D_structure/`**: Contains 2D structures extracted from the processed database.
- **`3D_structure/`**: Contains 3D structures extracted from the processed database.

### Processing Steps

#### STEP 1: Structure Extraction
**Script**: `1_get_the_structure.py`

**Description**:  
Extracts structures from the foundational database and removes cases that lack a structure prototype.

**Output**:
- **`1_with_structure.json`**: Database with materials that have defined structures.

#### STEP 2: Filtering Incorrect Cases
**Script**: `2_rm_wrong_case.py`

**Description**:  
Identifies and removes two-dimensional structures that may not correlate with the original three-dimensional structure.

**Output**:
- **`2_pass_formula.json`**: Filtered database with consistent 2D and 3D structures.

---
