import { useEffect, useState } from "react";
import { getPlexUser } from "@/services/PlexService.tsx";
import useClientIdentifier from "@/hooks/useClientIdentifier.tsx";
import { PlexToken } from "@/hooks/usePlexToken.tsx";
import { getSections } from "@/services/PMSService.tsx";

const usePMSSections = (serverUrl: string, plexToken: PlexToken) => {
  const [sections, setSections] = useState([]);

  useEffect(() => {
    if (!plexToken || !serverUrl) {
      setSections([]);
      return;
    }

    const fetchSections = async (): Promise<void> => {
      const sectionsData = await getSections(serverUrl, plexToken);
      setSections(sectionsData);
    };

    void fetchSections();
  }, [serverUrl, plexToken]);

  return sections;
};

export default usePMSSections;
