# Architecture Diagrams

Compact, left-to-right architecture diagrams optimized for GitHub rendering.

## Architecture Impact Diagram

Shows how `markdown-mermaid-writing` propagates as the foundation to all future skills.

```mermaid
flowchart LR
    subgraph Foundation["Foundation"]
        MM[markdown-mermaid-writing]
    end
    
    subgraph Standards["Standards"]
        MD[markdown guide]
        MG[mermaid guide]
        DT[diagram types]
        TM[templates]
    end
    
    subgraph Science["Science"]
        SW[scientific-writing]
        LR[literature-review]
        SS[schematics]
        SR[slides]
    end
    
    subgraph Engineering["Engineering"]
        AD[architecture]
        DS[database]
        API[APIs]
        INF[infrastructure]
    end
    
    subgraph Analysis["Analysis"]
        VIS[visualization]
        STAT[statistics]
        ML[machine-learning]
    end
    
    MM --> MD & MG & DT & TM
    MD --> SW & AD & DS
    MG --> SS & SR
    DT --> VIS & STAT & ML
    TM --> API & INF
```

## Key Points

- **Foundation**: Single source skill (`markdown-mermaid-writing`)
- **Standards**: Shared conventions across all domains
- **Propagation**: Every skill inherits documentation standards
- **Extensibility**: New skill categories follow established patterns

---

*Diagrams optimized for GitHub's Mermaid renderer*
