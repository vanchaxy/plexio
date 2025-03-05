/// <reference types="vite/client" />

declare global {
  const __APP_VERSION__: string;

  interface ImportMetaEnv {
    readonly VITE_LOCAL_DISCOVERY: string;
  }

  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }

  interface Window {
    env: {
      VITE_LOCAL_DISCOVERY: string;
    };
  }
}

export {};
