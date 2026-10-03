# PolicyDiff

A version-aware RAG project that retrieves, compares, and cites changes in platform privacy policies.

## Current progress

- Downloaded real Reddit Privacy Policy versions from Open Terms Archive
- Loaded and validated the source documents with Python
- Split the policies into 72 overlapping chunks
- Built a keyword-search baseline
- Installed tools for semantic search with embeddings

## Dataset

Source: Open Terms Archive Platform Governance Archive  
https://github.com/OpenTermsArchive/pga-versions

This project currently uses two versions of Reddit's Privacy Policy.