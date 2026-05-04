# Technical Architecture

This document outlines the internal engine logic and data orchestration layers of the **DeepClean OS**.

## Pipeline Orchestration

The diagram below represents the modernized flow of the DeepClean transformation engine. It utilizes a **Sequential Dependency Chain** to ensure each stage builds upon the previous one without data leakage.

```mermaid
graph TD
    %% Node Definitions
    Input[/CSV Payload/]
    
    subgraph DataIntegrity [Data Integrity Layer]
        Dup[Duplicate Scrubber]
    end
    
    subgraph FeatureEngineering [Feature Engineering Layer]
        Temp[Temporal Transformer]
        Ext[Feature Extraction: Y/M/D/W]
    end
    
    subgraph QualityControl [Quality Control Layer]
        Imp[Statistical Imputer]
        Out[Outlier Clipper]
    end
    
    subgraph Normalization [Model Readiness Layer]
        Enc[Categorical Encoder]
        Scale[Feature Scaler]
    end
    
    Output[/Cleaned Dataset/]

    %% Flow Connections
    Input --> Dup
    Dup --> Temp
    Temp --> Ext
    Ext --> Imp
    Imp --> Out
    Out --> Enc
    Enc --> Scale
    Scale --> Output

    %% Styling
    style Input fill:#0a0c10,stroke:#8892b0,stroke-width:2px,color:#fff
    style Output fill:#05070a,stroke:#00d4ff,stroke-width:3px,color:#00d4ff
    style DataIntegrity fill:rgba(0,212,255,0.05),stroke:#00d4ff,stroke-dasharray: 5 5
    style FeatureEngineering fill:rgba(0,212,255,0.05),stroke:#00d4ff,stroke-dasharray: 5 5
    style QualityControl fill:rgba(0,212,255,0.05),stroke:#00d4ff,stroke-dasharray: 5 5
    style Normalization fill:rgba(0,212,255,0.05),stroke:#00d4ff,stroke-dasharray: 5 5
```

## Transformation Logic Details

### 1. Integrity Layer
The **Duplicate Scrubber** performs an exact-row hash comparison to remove redundant data, ensuring that statistical measures like mean and variance are not skewed by repeated observations.

### 2. Engineering Layer
The **Temporal Transformer** converts string-based timestamps into high-resolution date components. This is critical for time-series analysis and allows standard models to learn from seasonal patterns.

### 3. Quality Layer
*   **Statistical Imputer**: Leverages Scikit-Learn's `SimpleImputer` to fill gaps without dropping rows.
*   **Outlier Clipper**: Applies a 3-Sigma Z-score boundary. Instead of removing outliers (which causes data loss), it "clips" them to the maximum acceptable boundary.

### 4. Readiness Layer
*   **Categorical Encoder**: Uses `LabelEncoder` to prepare non-numeric fields for mathematical processing.
*   **Feature Scaler**: The final step. It transforms the range of all numeric features (default: Z-score scaling) to prevent large numbers from dominating the model weights.
