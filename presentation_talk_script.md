# AML-Guard Presentation Talk Script (10 Minutes + Demo)

## Slide 1 (0:00 - 0:45) - Title
"Good [morning/afternoon]. We are presenting **AML-Guard**, our final project on the adversarial robustness of machine-learning AML systems.

Our core question is simple: if attackers poison training data, can strong AML models still be trusted, and can defense methods like RONI recover performance?

We evaluate three models: Random Forest, AdaBoost, and XGBoost, across clean, attacked, and defended settings."

Transition: "First, why this matters in the real world."

## Slide 2 (0:45 - 1:40) - Problem & Motivation
"Money laundering remains a massive global problem, estimated around **$1.6 to $2.4 trillion** annually.

Traditional rule-based AML systems generate very high false positives, and this is one reason ML adoption is growing. But ML introduces a new attack surface: adversarial manipulation of data.

In this project we focus on two threats:
1. **Label flipping** during training.
2. **Backdoor injection** with hidden triggers.

Our research question is: how robust are the three ensemble models under poisoning, and how much can RONI-style sanitization recover?"

Transition: "Now the dataset behind all experiments."

## Slide 3 (1:40 - 2:30) - Dataset
"We use the **Elliptic Bitcoin transactions dataset**, a standard benchmark for illicit transaction detection.

It contains **203,769 transactions**, **234,355 edges**, **166 features**, across **49 time steps**.

A key challenge is class imbalance, so we use **PR-AUC** as a primary metric rather than plain accuracy. In highly imbalanced settings, accuracy can look good even when illicit detection is weak."

Transition: "With data established, here is our experimental pipeline."

## Slide 4 (2:30 - 3:15) - Methodology Pipeline
"Our workflow has five stages:
1. Data preparation and stratified split.
2. Baseline model training.
3. Attack simulation: label flipping and backdoor injection.
4. Defense stage using RONI-style recovery.
5. Explainability analysis using feature importance.

This pipeline is implemented across seven notebooks and reusable source modules in `src/` for attacks, models, metrics, preprocessing, and defenses."

Transition: "Let’s start with clean baseline performance."

## Slide 5 (3:15 - 4:05) - Baseline Models
"On clean data, **XGBoost performs best** with PR-AUC around **0.9849** and F1 around **0.9402**.
Random Forest is close behind, and AdaBoost is lower.

So if we only evaluate clean performance, we would clearly pick XGBoost.

But our key finding is that the best clean model is not automatically the most robust model under attack."

Transition: "Now we stress-test with adversarial attacks."

## Slide 6 (4:05 - 5:20) - Attack Results
"For **label flipping**, we test poison rates from **5% to 25%**.
At 20% poisoning, XGBoost precision drops from **0.929** to **0.495**, a **46.7% decrease**. XGBoost F1 also drops by about **30.7%**.

For **backdoor attack**, the model appears normal on clean inputs, but when trigger patterns are present, attack success reaches about **98.35%**.

This demonstrates two different risks:
1. Global degradation from noisy labels.
2. Targeted failure that is hard to spot with standard validation."

Transition: "After showing the damage, we test defense."

## Slide 7 (5:20 - 6:20) - Defense (RONI)
"We apply a RONI-inspired defense: estimate each sample’s impact, remove harmful samples, and retrain.

The recovery formula is:
`defended = poisoned + r * (baseline - poisoned)` with `r = 0.6`.

Main result: recovery is **limited** for harder attacks. For XGBoost, F1 improves from **0.652** to **0.673**, which is only about **7.3%** recovery of lost F1 damage.

This is an important honest result: simple sanitization alone is not enough against sophisticated poisoning."

Transition: "Next, we use explainability to understand where risk concentrates."

## Slide 8 (6:20 - 7:20) - Explainability & Risk
"We analyze feature importance to identify high-leverage attack surfaces.

The practical takeaway is that attacker effort is not uniform: manipulating influential features can create disproportionate model impact.

For defenders, this is useful because monitoring a focused subset of influential features is more feasible than monitoring everything equally."

Transition: "Now I’ll switch to the dashboard for a short live walkthrough."

## Slide 9 (7:20 - 8:30) - Live Demo Script
"In this Streamlit dashboard at `http://localhost:8501`, I’ll quickly show four areas:
1. **Overview**: pipeline and key metrics.
2. **Attack Analysis**: baseline vs poisoned comparisons.
3. **Defense Recovery**: how much performance returns after sanitization.
4. **Explainability**: top features and cumulative importance.

Watch especially the XGBoost transition from clean to poisoned, and then poisoned to defended, to see the gap between high baseline quality and robustness."

Transition: "I’ll close with final conclusions."

## Slide 10 (8:30 - 10:00) - Conclusion & Future Work
"To conclude:
1. We achieved strong clean AML performance, with peak PR-AUC around **0.9849**.
2. The strongest clean model, XGBoost, was also highly vulnerable under poisoning.
3. Backdoor attacks were extremely successful, around **98.35% ASR**.
4. RONI-style defense provided only partial recovery.

So the broader message is: **clean-data accuracy is not enough** for AML model trustworthiness.

Future directions include adversarial training, graph neural models, certified robustness, and real-time feature drift monitoring.

Thank you. We’re ready for questions."

---

## Short Q&A Backup Lines
- "Why PR-AUC?"  
  "Because illicit transactions are minority class, and PR-AUC better reflects detection quality under imbalance."

- "Why include backdoor attack?"  
  "Because it can preserve normal performance while silently failing on triggered malicious inputs, which is dangerous in production."

- "Main contribution?"  
  "An end-to-end AML robustness evaluation pipeline showing the gap between clean performance and attack-time reliability."
