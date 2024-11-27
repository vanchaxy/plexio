import { useEffect, useState } from 'react';

export type PlexToken = string | null;

export interface SetPlexToken {
  (token: PlexToken): void;
}

const usePlexToken = (): [PlexToken, SetPlexToken] => {
  const [token, setToken] = useState<PlexToken>(() =>
    localStorage.getItem('plexToken'),
  );

  useEffect(() => {
    if (token) {
      localStorage.setItem('plexToken', token);
    } else {
      localStorage.removeItem('plexToken');
    }
  }, [token]);

  return [token, setToken];
};

export default usePlexToken;
