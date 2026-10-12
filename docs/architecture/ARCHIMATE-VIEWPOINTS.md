# ArchiMate-inspired Architecture Mapping

These diagrams are **ArchiMate-inspired**, not verified ArchiMate-conformant exchange models.

| Layer | Element | Relation |
|---|---|---|
| Motivation | Customer retention goal | Drives the churn prediction capability |
| Business | Retention analyst; churn review process | Consumes churn prediction service |
| Application | Prediction API; feature validation; inference pipeline | Serves retention workflow |
| Data | Customer attributes; model artifact; evaluation results | Read/produced by application components |
| Technology | Container image; Kubernetes/OpenShift; observability | Hosts and monitors application |
| Implementation & Migration | Baseline → pilot → production | Incremental delivery |

## Traceability
Business requirement → API contract → model metric → CI control → operational alert.

## Trust boundaries
Authorized external client → gateway → inference namespace → immutable model artifact. Identity enforcement at the gateway is an **architecture requirement**, not implemented by the FastAPI service itself.

## Diagram index
Enterprise, logical, technical, C4 context/container/component, data flow, security, deployment, observability and multi-cloud are in `diagrams/source` with editable Mermaid and SVG/PNG renderings.
