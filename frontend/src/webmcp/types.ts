export type SearchProductsInput = {
  query: string;
  max_price?: number;
};

export type MirrorToolInput = Record<string, unknown>;

export type MirrorToolContext = {
  signal: AbortSignal;
};

export type MirrorToolDecision =
  | "ALLOW"
  | "APPROVAL_REQUIRED"
  | "DENY";

export type MirrorAuthorizationResult = {
  decision: MirrorToolDecision;
  risk_level?: string;
  drift_score?: number;
  reason_codes?: string[];
  explanation?: string;
  approval_id?: string | null;
};