import { createRoot } from "react-dom/client";

import { ScoreDistributions } from "@/components/evaluations/score-distributions";
import { PageHeader } from "@/components/ui/page-header";

import "../src/styles.css";

const variants = [{ id: "base", label: "Base model" }];
const comparisonVariants = [
  { id: "base", label: "Base model" },
  { id: "trained", label: "Trained model" },
  { id: "reference", label: "Reference model" },
];
const cases = [
  {
    metrics: ["SOC task success · generative", "SOC task success · jev"],
    scores: [
      { name: "SOC task success · generative", value: 0.5, variant: "base" },
      { name: "SOC task success · generative", value: 0.75, variant: "base" },
      { name: "SOC task success · jev", value: 0.5, variant: "base" },
      { name: "SOC task success · jev", value: 1, variant: "base" },
    ],
    title: "Two evaluators",
    variants,
  },
  {
    metrics: ["Zero score", "Perfect score"],
    scores: [
      { name: "Zero score", value: 0, variant: "base" },
      { name: "Perfect score", value: 1, variant: "base" },
    ],
    title: "Boundary values",
    variants,
  },
  {
    metrics: ["Task success", "Long evaluator name with detailed structured output checks"],
    scores: comparisonVariants.flatMap((variant) =>
      ["Task success", "Long evaluator name with detailed structured output checks"].flatMap(
        (name) => [0.25, 0.5, 0.75, 1].map((value) => ({ name, value, variant: variant.id }))
      )
    ),
    title: "Model comparison",
    variants: comparisonVariants,
  },
];

function Preview() {
  return (
    <main className="mx-auto max-w-6xl space-y-5 p-4">
      <PageHeader
        description="Synthetic scores. No evaluation or provider call."
        title="Evaluation chart fixtures"
      />
      {cases.map(({ title, ...props }) => (
        <section aria-label={title} key={title}>
          <ScoreDistributions {...props} />
        </section>
      ))}
    </main>
  );
}

const root = createRoot(document.getElementById("app")!);
root.render(<Preview />);
import.meta.hot?.dispose(() => root.unmount());
