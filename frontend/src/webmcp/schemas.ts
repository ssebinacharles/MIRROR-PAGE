export const searchProductsSchema = {
  type: 'object',
  properties: { query: { type: 'string', description: 'Search terms' }, max_price: { type: 'number', description: 'Maximum price' } },
  required: ['query'], additionalProperties: false,
} as const;
export const productDetailsSchema = { type: 'object', properties: { product_id: { type: 'string' } }, required: ['product_id'], additionalProperties: false } as const;
export const compareProductsSchema = { type: 'object', properties: { product_ids: { type: 'array', items: { type: 'string' } } }, required: ['product_ids'], additionalProperties: false } as const;
export const purchaseProductSchema = { type: 'object', properties: { product_id: { type: 'string' } }, required: ['product_id'], additionalProperties: false } as const;
