import { useEffect, useState } from 'react';
import { registerMirrorTools } from '@/webmcp/registry';
import { webmcpSupported } from '@/webmcp/compatibility';
export function useWebMCP() {
  const [registered, setRegistered] = useState(false);
  useEffect(() => { registerMirrorTools().then(setRegistered).catch(() => setRegistered(false)); }, []);
  return { supported: webmcpSupported(), registered };
}
