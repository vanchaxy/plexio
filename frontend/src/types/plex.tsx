interface AuthPin {
  id: string;
  code: string;
}

interface PlexUser {
  username: string;
  thumb: string;
}

interface PlexServer {
  name: string;
  sourceTitle: string | null;
  publicAddress: string;
  accessToken: string;
  relay: boolean;
  httpsRequired: boolean;
  connections: any[];
}
