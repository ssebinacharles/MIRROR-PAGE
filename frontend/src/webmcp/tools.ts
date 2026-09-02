import { api } from '@/services/api';
import { searchProductsSchema, productDetailsSchema, compareProductsSchema, purchaseProductSchema } from './schemas';

const products = [
  { id: 'p1', name: 'Mirror DevStation 14', price: 999, cpu: 'Ryzen 7', ram: 32, storage: '1TB NVMe' },
  { id: 'p2', name: 'Mirror DevStation 15', price: 1099, cpu: 'Core Ultra 7', ram: 32, storage: '1TB NVMe' },
  { id: 'p3', name: 'Mirror ComputeBook 16', price: 1199, cpu: 'Ryzen 9', ram: 64, storage: '2TB NVMe' },
  { id: 'p4', name: 'Mirror LiteDev 13', price: 749, cpu: 'Core Ultra 5', ram: 16, storage: '512GB NVMe' },
];

export function findProducts(query: string, maxPrice?: number) {
  const q = query.toLowerCase();
  return products.filter((p) => p.name.toLowerCase().includes(q) || p.cpu.toLowerCase().includes(q) || !q).filter((p) => maxPrice == null || p.price <= maxPrice);
}

export const toolDefinitions = {
  search_products: {
    title: 'Search Products',
    description: 'Search the MIRROR synthetic product catalog.',
    inputSchema: searchProductsSchema,
    annotations: { readOnlyHint: true },
    execute: async (input: { query: string; max_price?: number }) => ({ products: findProducts(input.query, input.max_price) }),
  },
  get_product_details: {
    title: 'Get Product Details', description: 'Return details for a product.', inputSchema: productDetailsSchema, annotations: { readOnlyHint: true },
    execute: async (input: { product_id: string }) => products.find((p) => p.id === input.product_id) ?? { error: 'Product not found' },
  },
  compare_products: {
    title: 'Compare Products', description: 'Compare several catalog products.', inputSchema: compareProductsSchema, annotations: { readOnlyHint: true },
    execute: async (input: { product_ids: string[] }) => ({ products: products.filter((p) => input.product_ids.includes(p.id)) }),
  },
  purchase_product: {
    title: 'Purchase Product', description: 'Simulate a consequential product purchase through MIRROR authorization.', inputSchema: purchaseProductSchema,
    annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: true },
    execute: async (input: { product_id: string }) => {
      const intentId = new URLSearchParams(window.location.search).get('intent') || undefined;
      const agentId = new URLSearchParams(window.location.search).get('agent') || undefined;
      if (!intentId || !agentId) return { status: 'blocked', reason: 'MIRROR context is required before a purchase can execute.', product_id: input.product_id };
      const result = await api.evaluateAction({ intent_contract_id: intentId, tool_name: 'purchase_product', agent_id: agentId, input_payload: input, execute: false });
      return result;
    },
  },
};
