import { useCallback, useEffect, useState } from "react";

import {
  isWebMCPSupported,
} from "@/webmcp/compatibility";

import {
  registerMirrorTools,
} from "@/webmcp/registry";

export function useWebMCP() {
  const [supported, setSupported] =
    useState(false);

  const [registered, setRegistered] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const register = useCallback(async () => {
    setError(null);

    const available = isWebMCPSupported();

    setSupported(available);

    if (!available) {
      setRegistered(false);
      return;
    }

    try {
      await registerMirrorTools();

      setRegistered(true);
    } catch (err) {
      console.error(
        "[MIRROR] WebMCP registration failed:",
        err,
      );

      setRegistered(false);

      setError(
        err instanceof Error
          ? err.message
          : "WebMCP registration failed.",
      );
    }
  }, []);

  useEffect(() => {
    void register();
  }, [register]);

  return {
    supported,
    registered,
    error,
    register,
  };
}