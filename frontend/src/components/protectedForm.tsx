import { FC } from 'react';
import ConfigurationForm from '@/components/configurationForm';
import Loading from '@/components/loading.tsx';
import Login from '@/components/login.tsx';
import usePlexServers from '@/hooks/usePlexServers.tsx';

interface Props {
  plexToken: string | null;
  plexUser: PlexUser | null | undefined;
}

const ProtectedForm: FC<Props> = ({ plexToken, plexUser }) => {
  const servers = usePlexServers(plexToken);

  if (plexUser === null) {
    return <Login />;
  }

  if (plexUser === undefined || !servers.length) {
    return <Loading />;
  }

  return <ConfigurationForm servers={servers} />;
};

export default ProtectedForm;
