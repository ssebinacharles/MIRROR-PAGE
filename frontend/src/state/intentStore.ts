import type { IntentContract } from '@/types/models';

const demoIntent: IntentContract = {
  id: 'demo-intent',
  version: 1,
  goal: 'Research development laptops under $1,200. Do not purchase anything.',
  constraints: { max_price: 1200, currency: 'USD' },
  allowed_actions: ['search_products', 'get_product_details', 'compare_products'],
  approval_required_actions: ['add_to_cart'],
  denied_actions: ['purchase_product'],
  data_scope: ['public_product_information'],
  status: 'ACTIVE',
  expires_at: new Date(Date.now() + 60 * 60 * 1000).toISOString(),
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
};
let current = demoIntent;
export function useIntentStore(selector: (state: { intent: IntentContract }) => IntentContract) {
  return selector({ intent: current });
}
export function setDemoIntent(intent: IntentContract) { current = intent; }
