export function isWebMCPSupported(): boolean {
  return (
    typeof document !== "undefined" &&
    "modelContext" in document
  );
}

export function getWebMCPStatus():
  | "AVAILABLE"
  | "UNAVAILABLE" {
  return isWebMCPSupported()
    ? "AVAILABLE"
    : "UNAVAILABLE";
}