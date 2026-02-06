import { useCallback, useMemo, useState } from 'react';

const ADMIN_STORAGE_KEY = 'plexio.admin.credentials';
const ADMIN_AUTH_KEY = 'plexio.admin.authenticated';

interface AdminConfig {
  username: string;
  passwordHash: string;
}

interface AuthResult {
  success: boolean;
  error?: string;
}

const loadAdminConfig = (): AdminConfig | null => {
  const stored = localStorage.getItem(ADMIN_STORAGE_KEY);
  if (!stored) {
    return null;
  }

  try {
    return JSON.parse(stored) as AdminConfig;
  } catch (error) {
    console.error('Unable to parse admin credentials', error);
    return null;
  }
};

const hashValue = async (value: string): Promise<string> => {
  if (!window.crypto?.subtle) {
    return btoa(value);
  }

  const encoder = new TextEncoder();
  const data = encoder.encode(value);
  const hashBuffer = await window.crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map((item) => item.toString(16).padStart(2, '0')).join('');
};

const useAdminAuth = () => {
  const [adminConfig, setAdminConfig] = useState<AdminConfig | null>(() =>
    loadAdminConfig(),
  );
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(
    () => sessionStorage.getItem(ADMIN_AUTH_KEY) === 'true',
  );

  const configureAdmin = useCallback(
    async (username: string, password: string): Promise<AuthResult> => {
      if (!username || !password) {
        return { success: false, error: 'Username and password are required.' };
      }

      const passwordHash = await hashValue(password);
      const updatedConfig = { username, passwordHash };

      localStorage.setItem(ADMIN_STORAGE_KEY, JSON.stringify(updatedConfig));
      setAdminConfig(updatedConfig);
      setIsAuthenticated(true);
      sessionStorage.setItem(ADMIN_AUTH_KEY, 'true');

      return { success: true };
    },
    [],
  );

  const authenticate = useCallback(
    async (username: string, password: string): Promise<AuthResult> => {
      if (!adminConfig) {
        return { success: false, error: 'Admin credentials are not set.' };
      }

      const passwordHash = await hashValue(password);

      if (
        adminConfig.username !== username ||
        adminConfig.passwordHash !== passwordHash
      ) {
        return { success: false, error: 'Invalid username or password.' };
      }

      setIsAuthenticated(true);
      sessionStorage.setItem(ADMIN_AUTH_KEY, 'true');

      return { success: true };
    },
    [adminConfig],
  );

  const logout = useCallback(() => {
    setIsAuthenticated(false);
    sessionStorage.removeItem(ADMIN_AUTH_KEY);
  }, []);

  const adminUsername = useMemo(
    () => adminConfig?.username ?? null,
    [adminConfig?.username],
  );

  return {
    adminConfig,
    adminUsername,
    authenticate,
    configureAdmin,
    isAuthenticated,
    logout,
  };
};

export default useAdminAuth;
