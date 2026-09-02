import { toolDefinitions } from './tools';
import { webmcpSupported } from './compatibility';

let registered = false;

export async function registerMirrorTools() {
  if (registered || !webmcpSupported()) return false;
  const context = (document as Document & { modelContext: any }).modelContext;
  for (const [name, tool] of Object.entries(toolDefinitions)) {
    await context.registerTool({
      name,
      title: tool.title,
      description: tool.description,
      inputSchema: tool.inputSchema,
      annotations: tool.annotations,
      execute: tool.execute,
    });
  }
  registered = true;
  return true;
}
