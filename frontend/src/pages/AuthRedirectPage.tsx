import { FC, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import Loading from '@/components/loading.tsx';
import useClientIdentifier from '@/hooks/useClientIdentifier.tsx';
import { SetPlexToken } from '@/hooks/usePlexToken.tsx';
import { getAuthToken } from '@/services/PlexService.tsx';

interface Props {
  setPlexToken: SetPlexToken;
}

const AuthRedirectPage: FC<Props> = ({ setPlexToken }) => {
  const [searchParams] = useSearchParams();
  const clientIdentifier = useClientIdentifier();
  const navigate = useNavigate();

  useEffect(() => {
    if (!clientIdentifier) return;

    const { id, code, redirect } = Object.fromEntries(searchParams.entries());

    const setAuthToken = async (): Promise<void> => {
      const authToken = await getAuthToken(
        { id: id, code: code },
        clientIdentifier,
      );
      setPlexToken(authToken);
    };

    void setAuthToken();
    navigate(redirect);
  }, [searchParams, clientIdentifier, navigate]);

  return <Loading />;
};

export default AuthRedirectPage;
