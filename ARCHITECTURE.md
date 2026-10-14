# MindCheck Week 1 Architecture

```mermaid
flowchart LR
    A[Generated synthetic check-ins CSV] --> B[Load and validate data]
    B --> C[Split by synthetic student and date]
    C --> D[Baseline window: first 7 observations]
    C --> E[Recent window: latest 3 observations]
    D --> F[Transparent threshold rules]
    E --> F
    F --> G[Indicator-by-indicator explanation]
    G --> H[Streamlit dashboard and CSV export]
    I[Evaluation scenario labels] -. separate; not a rule input .-> J[Manual/test-suite evaluation]
```

## Week 1 boundary

No hardware, cloud service, real student records, predictive-model training, or LLM is required for this milestone. The goal is a simple and inspectable end-to-end software proof-of-concept.
