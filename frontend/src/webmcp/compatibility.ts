export function webmcpSupported() { return typeof document !== 'undefined' && 'modelContext' in document; }
