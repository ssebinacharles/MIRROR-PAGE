export type Product = {
  id: string;
  name: string;
  description: string;
  category: string;
  price: string;
  currency: string;
  specs: Record<string, unknown>;
  available: boolean;
  created_at: string;
};