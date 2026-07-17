# Research

Detailed write-ups of the applied research referenced in the top-level README.

## Hound ML

**Genomic AMR (Antimicrobial Resistance) Prediction in *E. coli***

**Code & full results:** [github.com/YashovardhanB28/hound-ml](https://github.com/YashovardhanB28/hound-ml)

End-to-end ML pipeline predicting resistance to ciprofloxacin, ceftazidime, and meropenem using
~1,000 public *E. coli* genomes from BacBench.

- **Pipeline:** raw whole-genome assemblies → AMRFinderPlus → binary gene presence/absence
  matrices → mapped to phenotypic MIC metadata.
- **Models:** class-balanced Random Forest and Logistic Regression.
- **Results:** ~94–98% accuracy, AUROC up to 0.99.
- **Interpretability:** top feature importances matched known biological mechanisms — e.g.
  ESBLs/AmpC for ceftazidime, carbapenemases (blaKPC-3) for meropenem, MDR plasmid/integron
  signatures for ciprofloxacin.

## NETRS Signature

**NSCLC NETosis Prognostic Signature (Oncology / Genomics)**

An 18-gene prognostic signature (NETRS) for non-small cell lung cancer survival, built via LASSO
Cox regression (10-fold CV) on TCGA-LUAD bulk RNA-seq and clinical metadata.

- **Validation:** external cohorts GSE72094 and GSE31210 (~400 patients), Kaplan-Meier split
  p < 0.0001, ROC AUC 0.697 on unseen data.
- **Clinical impact:** multivariate Cox models show High-NETRS patients have ~3x mortality risk
  (HR = 2.92, p = 0.001), independent of stage, age, and gender.
- **Mechanism:** scRNA-seq + CellChat mapped how NETosis-undergoing tumor-associated neutrophils
  rewire the immunosuppressive tumor microenvironment via CXCL and TGF-β signaling.

## Deepfake Forensics

**Generalization Gap Analysis in CNN-based Deepfake Detection**

Computer vision pipeline (PyTorch, EfficientNet-B1, OpenCV) processing 50,000+ frames at
230ms/frame on consumer hardware.

- **Benchmark:** 97% accuracy on FaceForensics++ (academic dataset).
- **Real-world stress test:** accuracy dropped to 30% on compressed social media video
  (YouTube/TikTok) — a critical generalization gap.
- **Fix:** domain-specific fine-tuning recovered real-world accuracy to >80%.
- **Explainability:** Grad-CAM heatmaps visualize the CNN's decision-making, supporting
  transparent AI safety auditing. Open-sourced to support responsible AI research.

---

*Have a question about methodology or want the underlying data/code for any of these — reach out
via [LinkedIn](https://www.linkedin.com/in/yashovardhan-bangur) or email.*
