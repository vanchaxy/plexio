import { useEffect, useState } from "react";
import { getPlexUser } from "@/services/PlexService.tsx";
import useClientIdentifier from "@/hooks/useClientIdentifier.tsx";
import { PlexToken } from "@/hooks/usePlexToken.tsx";

const usePlexUser = (plexToken: PlexToken) => {
  const [user, setUser] = useState<undefined | null | PlexUser>();
  const clientIdentifier = useClientIdentifier();

  useEffect(() => {
    if (!clientIdentifier) return;
    if (!plexToken) {
      setUser(null);
      return;
    }

    const fetchPlexUser = async (): Promise<void> => {
      const userData = await getPlexUser(plexToken, clientIdentifier);
      setUser(userData);
    };

    void fetchPlexUser();
  }, [clientIdentifier, plexToken]);

  return user;
};

export default usePlexUser;
