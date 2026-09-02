import { beforeEach, describe, expect, it, vi } from 'vitest';
import { registerMirrorTools } from '@/webmcp/registry';

function installMockModelContext() {
  const registerTool = vi.fn().mockResolvedValue(undefined);
  Object.defineProperty(document, 'modelContext', {
    configurable: true,
    value: { registerTool },
  });
  return registerTool;
}

describe('registerMirrorTools', () => {
  beforeEach(() => {
    vi.resetModules();
    delete (document as Document & { modelContext?: unknown }).modelContext;
  });

  it('registers the configured MIRROR tools when WebMCP is available', async () => {
    const registerTool = installMockModelContext();
    const { registerMirrorTools: freshRegister } = await import('@/webmcp/registry');

    const registered = await freshRegister();

    expect(registered).toBe(true);
    expect(registerTool).toHaveBeenCalled();

    const names = registerTool.mock.calls.map((call) => call[0]?.name);
    expect(names).toEqual(expect.arrayContaining([
      'search_products',
      'get_product_details',
      'compare_products',
      'purchase_product',
    ]));
  });

  it('does nothing when WebMCP is unavailable', async () => {
    const { registerMirrorTools: freshRegister } = await import('@/webmcp/registry');
    await expect(freshRegister()).resolves.toBe(false);
  });
});
