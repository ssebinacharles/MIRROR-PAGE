import { authorizeTool } from "./authorize";
import type { SearchProductsInput } from "./types";
import type { Product } from "@/types/product";

const API_URL =
  import.meta.env.VITE_API_URL ??
  "http://127.0.0.1:8000/api";

function getModelContext() {
  if (
    typeof document === "undefined" ||
    !("modelContext" in document)
  ) {
    return null;
  }

  return document.modelContext;
}

async function searchProducts(
  input: SearchProductsInput,
): Promise<{ count: number; products: Product[] }> {
  const response = await fetch(
    `${API_URL}/products/search/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(input),
    },
  );

  if (!response.ok) {
    const message = await response.text();

    throw new Error(
      `Product search failed (${response.status}): ${message}`,
    );
  }

  return response.json();
}

async function getProductDetails(
  productId: string,
): Promise<Product> {
  const response = await fetch(
    `${API_URL}/products/${productId}/`,
  );

  if (!response.ok) {
    const message = await response.text();

    throw new Error(
      `Product lookup failed (${response.status}): ${message}`,
    );
  }

  return response.json();
}

export async function registerTools(): Promise<void> {
  const modelContext = getModelContext();

  if (!modelContext) {
    console.info(
      "[MIRROR] WebMCP is unavailable in the current browser.",
    );

    return;
  }

  /*
   * ---------------------------------------------------------
   * search_products
   * ---------------------------------------------------------
   *
   * Read-only WebMCP capability.
   *
   * Flow:
   *
   * Agent
   *   ↓
   * WebMCP
   *   ↓
   * MIRROR authorization
   *   ↓
   * Django product search
   */

  await modelContext.registerTool({
    name: "search_products",
    title: "Search Products",
    description:
      "Search the MIRROR synthetic product catalog by query and optional maximum price.",
    inputSchema: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description:
            "Product name, category, feature, or capability to search for.",
        },
        max_price: {
          type: "number",
          description:
            "Optional maximum product price.",
        },
      },
      required: ["query"],
      additionalProperties: false,
    },
    annotations: {
      readOnlyHint: true,
    },

    execute: async (input: SearchProductsInput) => {
      const decision = await authorizeTool(
        "search_products",
        input,
      );

      if (decision.decision !== "ALLOW") {
        return JSON.stringify({
          status: "blocked",
          mirror: decision,
        });
      }

      const result = await searchProducts(input);

      return JSON.stringify({
        status: "authorized",
        mirror: decision,
        ...result,
      });
    },
  });

  /*
   * ---------------------------------------------------------
   * get_product_details
   * ---------------------------------------------------------
   */

  await modelContext.registerTool({
    name: "get_product_details",
    title: "Get Product Details",
    description:
      "Retrieve detailed information about a specific MIRROR product.",
    inputSchema: {
      type: "object",
      properties: {
        product_id: {
          type: "string",
          description:
            "UUID of the product to retrieve.",
        },
      },
      required: ["product_id"],
      additionalProperties: false,
    },
    annotations: {
      readOnlyHint: true,
    },

    execute: async (input: {
      product_id: string;
    }) => {
      const decision = await authorizeTool(
        "get_product_details",
        input,
      );

      if (decision.decision !== "ALLOW") {
        return JSON.stringify({
          status: "blocked",
          mirror: decision,
        });
      }

      const product = await getProductDetails(
        input.product_id,
      );

      return JSON.stringify({
        status: "authorized",
        mirror: decision,
        product,
      });
    },
  });

  /*
   * ---------------------------------------------------------
   * compare_products
   * ---------------------------------------------------------
   *
   * This is deliberately read-only.
   */

  await modelContext.registerTool({
    name: "compare_products",
    title: "Compare Products",
    description:
      "Compare multiple MIRROR products by their specifications and prices.",
    inputSchema: {
      type: "object",
      properties: {
        product_ids: {
          type: "array",
          description:
            "List of product UUIDs to compare.",
          items: {
            type: "string",
          },
          minItems: 2,
        },
      },
      required: ["product_ids"],
      additionalProperties: false,
    },
    annotations: {
      readOnlyHint: true,
    },

    execute: async (input: {
      product_ids: string[];
    }) => {
      const decision = await authorizeTool(
        "compare_products",
        input,
      );

      if (decision.decision !== "ALLOW") {
        return JSON.stringify({
          status: "blocked",
          mirror: decision,
        });
      }

      const products = await Promise.all(
        input.product_ids.map((id) =>
          getProductDetails(id),
        ),
      );

      return JSON.stringify({
        status: "authorized",
        mirror: decision,
        products,
      });
    },
  });

  /*
   * ---------------------------------------------------------
   * purchase_product
   * ---------------------------------------------------------
   *
   * Consequential action.
   *
   * IMPORTANT:
   * We do NOT execute a real purchase here.
   *
   * MIRROR must first evaluate:
   *
   *   intent
   *   ↓
   *   policy
   *   ↓
   *   drift
   *   ↓
   *   approval
   *
   * The backend will later provide the synthetic execution
   * endpoint after the approval workflow is complete.
   */

  await modelContext.registerTool({
    name: "purchase_product",
    title: "Purchase Product",
    description:
      "Purchase a product from the MIRROR synthetic marketplace. This is a consequential action and may require explicit human approval.",
    inputSchema: {
      type: "object",
      properties: {
        product_id: {
          type: "string",
          description:
            "UUID of the product to purchase.",
        },
        quantity: {
          type: "integer",
          description:
            "Number of units to purchase.",
          minimum: 1,
          default: 1,
        },
      },
      required: ["product_id"],
      additionalProperties: false,
    },
    annotations: {
      readOnlyHint: false,
    },

    execute: async (input: {
      product_id: string;
      quantity?: number;
    }) => {
      const decision = await authorizeTool(
        "purchase_product",
        input,
      );

      if (decision.decision === "DENY") {
        return JSON.stringify({
          status: "blocked",
          mirror: decision,
        });
      }

      if (
        decision.decision ===
        "APPROVAL_REQUIRED"
      ) {
        return JSON.stringify({
          status: "approval_required",
          mirror: decision,
        });
      }

      /*
       * DO NOT perform real commerce.
       *
       * The synthetic purchase execution endpoint will
       * be added after the approval workflow is complete.
       */

      return JSON.stringify({
        status: "authorized",
        message:
          "Purchase authorization granted. Synthetic execution will be handled by MIRROR.",
        mirror: decision,
      });
    },
  });

  console.info(
    "[MIRROR] WebMCP tools registered:",
    [
      "search_products",
      "get_product_details",
      "compare_products",
      "purchase_product",
    ],
  );
}