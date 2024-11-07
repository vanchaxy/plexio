import axios from "axios";

export const getSections = async (
  serverUrl: string,
  token: string,
): Promise<PlexServer[]> => {
  try {
    const response = await axios.get(`${serverUrl}/library/sections`, {
      params: {
        "X-Plex-Token": token,
      },
    });

    const sections = response.data?.MediaContainer?.Directory;

    if (!Array.isArray(sections)) {
      throw new Error("Invalid response from server");
    }

    return sections.filter((section: any) =>
      ["show", "movie"].includes(section?.type),
    );
  } catch (error) {
    console.error("Error fetching Plex servers:", error);
    throw error;
  }
};
