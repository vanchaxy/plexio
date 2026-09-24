import axios from 'axios';

const PLEX_PRODUCT_NAME = 'Plexio';
const PLEX_API_URL = 'https://plex.tv/api/v2';
// Plex's v2 API defaults to XML unless JSON is explicitly requested.
const JSON_HEADERS = { Accept: 'application/json' };

export const createAuthPin = async (
  clientIdentifier: string,
): Promise<AuthPin> => {
  try {
    const response = await axios.postForm(
      `${PLEX_API_URL}/pins`,
      {
        strong: 'true',
        'X-Plex-Product': PLEX_PRODUCT_NAME,
        'X-Plex-Client-Identifier': clientIdentifier,
      },
      { headers: JSON_HEADERS },
    );

    return response.data;
  } catch (error) {
    console.error('Error fetching users:', error);
    throw error;
  }
};

export const getAuthToken = async (
  authPin: AuthPin,
  clientIdentifier: string,
): Promise<string> => {
  try {
    const response = await axios.get(`${PLEX_API_URL}/pins/${authPin.id}`, {
      params: {
        code: authPin.code,
        'X-Plex-Client-Identifier': clientIdentifier,
      },
      headers: JSON_HEADERS,
    });
    return response.data.authToken;
  } catch (error) {
    console.error('Error auth token:', error);
    throw error;
  }
};

export const getPlexUser = async (
  token: string,
  clientIdentifier: string,
): Promise<PlexUser | null> => {
  try {
    const response = await axios.get(`${PLEX_API_URL}/user`, {
      params: {
        'X-Plex-Product': PLEX_PRODUCT_NAME,
        'X-Plex-Client-Identifier': clientIdentifier,
        'X-Plex-Token': token,
      },
      headers: JSON_HEADERS,
    });

    if (response.status !== 200) {
      return null;
    }

    return response.data;
  } catch (error) {
    console.error('Error fetching user:', error);
    return null;
  }
};

export const getPlexServers = async (
  token: string,
  clientIdentifier: string,
): Promise<PlexServer[]> => {
  try {
    const response = await axios.get(`${PLEX_API_URL}/resources`, {
      params: {
        includeHttps: 1,
        includeRelay: 1,
        'X-Plex-Token': token,
        'X-Plex-Client-Identifier': clientIdentifier,
      },
      headers: JSON_HEADERS,
    });

    if (!response.data || !Array.isArray(response.data)) {
      throw new Error('Invalid response from server');
    }

    return response.data.filter(
      (server: any) =>
        server.provides.includes('server') && 'accessToken' in server,
    );
  } catch (error) {
    console.error('Error fetching Plex servers:', error);
    throw error;
  }
};
