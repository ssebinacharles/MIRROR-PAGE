import { registerTools } from "./tools";

let registered = false;

export async function registerMirrorTools(): Promise<void> {
  if (registered) {
    return;
  }

  if (
    typeof document === "undefined" ||
    !("modelContext" in document)
  ) {
    console.info(
      "[MIRROR] WebMCP is not available in this browser.",
    );
    return;
  }

  try {
    await registerTools();

    registered = true;

    console.info(
      "[MIRROR] WebMCP tools registered successfully.",
    );
  } catch (error) {
    console.error(
      "[MIRROR] WebMCP registration failed:",
      error,
    );

    throw error;
  }
}