import { useEffect, useState } from 'react';
import useClientIdentifier from '@/hooks/useClientIdentifier.tsx';
import { PlexToken } from '@/hooks/usePlexToken.tsx';
import { getPlexServers } from '@/services/PlexService.tsx';

const usePlexServers = (plexToken: PlexToken | null) => {
  const [servers, setServers] = useState<PlexServer[]>([]);
  const clientIdentifier = useClientIdentifier();

  useEffect(() => {
    if (!clientIdentifier || !plexToken) return;

    const fetchPlexServers = async (): Promise<void> => {
      const plexServers = await getPlexServers(plexToken, clientIdentifier);
      setServers(plexServers);
    };

    void fetchPlexServers();
  }, [clientIdentifier, plexToken]);

  return servers;
};

export default usePlexServers;
