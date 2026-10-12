import { useId } from "react";

import { EntityRef } from "@/components/entity-ref";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { useFinetuningJobQuery } from "@/hooks/use-finetuning";
import type { FinetuningJobList } from "@/openapi";

type LabelSet = {
  question: string;
  kind: string;
  options: string[];
  option_values: number[] | null;
};

function DatasetLabels({
  job,
  showDataset,
  datasetName,
}: {
  job: FinetuningJobList;
  showDataset: boolean;
  datasetName?: string;
}) {
  const query = useFinetuningJobQuery(job.id);
  const summary = query.data?.record?.prediction_labels;
  const groups: LabelSet[] = summary?.label_sets ?? [];
  return (
    <div className="flex min-w-0 flex-col items-end gap-1">
      {showDataset && (
        <EntityRef id={job.dataset} kind="dataset" name={datasetName} projectId={job.project} />
      )}
      {query.isPending ? (
        <Skeleton className="h-5 w-20 max-w-full" />
      ) : query.error || summary?.state !== "available" ? (
        <p className="text-muted-foreground">Unavailable</p>
      ) : groups.length === 0 ? (
        <p className="text-muted-foreground">Not recorded</p>
      ) : (
        <div className="flex max-h-60 max-w-full flex-col items-end gap-2 overflow-y-auto">
          {groups.map((group, index) => (
            <div className="flex min-w-0 max-w-full flex-col items-end gap-1" key={index}>
              {groups.length > 1 && (
                <p className="text-right text-muted-foreground [overflow-wrap:anywhere]">
                  {group.question}
                </p>
              )}
              <ul
                aria-label={group.question}
                className="flex min-w-0 max-w-full flex-wrap justify-end gap-1"
                title={group.question}
              >
                {group.options.map((option, optionIndex) => (
                  <li className="min-w-0 max-w-full" key={option}>
                    <Badge
                      className="h-auto min-h-5 max-w-full bg-control px-1.5 whitespace-normal py-0.5 leading-4 [overflow-wrap:anywhere]"
                      size="chip"
                      variant="secondary"
                    >
                      <span className="min-w-0">{option}</span>
                      {group.option_values && (
                        <span className="ml-1.5 shrink-0 border-l border-border pl-1.5 tabular-nums text-muted-foreground">
                          {group.option_values[optionIndex]}
                        </span>
                      )}
                    </Badge>
                  </li>
                ))}
              </ul>
            </div>
          ))}
          {summary.total_sets > groups.length && (
            <p className="text-muted-foreground">
              {groups.length} of {summary.total_sets} label sets
            </p>
          )}
        </div>
      )}
    </div>
  );
}

export function PredictionLabels({
  jobs,
  datasetNames,
}: {
  jobs: FinetuningJobList[];
  datasetNames?: Map<string, string>;
}) {
  const heading = useId();
  const datasets = [...new Map(jobs.map((job) => [job.cell ?? job.id, job])).values()];
  if (!datasets.length) return null;
  return (
    <div aria-labelledby={heading} className="flex max-w-full items-baseline gap-2" role="group">
      <dt className="shrink-0 text-muted-foreground" id={heading}>
        Prediction labels
      </dt>
      <dd className="flex min-w-0 max-w-[240px] flex-col gap-2">
        {datasets.map((job) => (
          <DatasetLabels
            datasetName={datasetNames?.get(job.dataset)}
            job={job}
            key={job.cell ?? job.id}
            showDataset={datasets.length > 1}
          />
        ))}
      </dd>
    </div>
  );
}
