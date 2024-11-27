import { Button } from '@/components/ui/button.tsx';
import useClientIdentifier from '@/hooks/useClientIdentifier.tsx';
import { createAuthPin } from '@/services/PlexService.tsx';

const Login = () => {
  const clientIdentifier = useClientIdentifier();

  const handleLogin = async () => {
    const { origin, pathname } = window.location;

    const authPin = await createAuthPin(clientIdentifier);
    const currentPath = encodeURIComponent(pathname);

    const redirectParams = `code=${authPin.code}&id=${authPin.id}&redirect=${currentPath}`;
    const forwardUrl = encodeURIComponent(
      `${origin}/auth-redirect?${redirectParams}`,
    );

    const loginParams = `code=${authPin.code}&forwardUrl=${forwardUrl}&clientID=${clientIdentifier}`;
    window.location.href = `https://app.plex.tv/auth#?${loginParams}`;
  };

  return (
    <div className="border rounded-lg p-6">
      <h1 className="text-xl font-bold text-center ">
        Plexio: Plex Interaction for Stremio
      </h1>
      <p className="text-sm text-center mt-2">
        Seamlessly connects your Plex and Stremio accounts, letting you enjoy
        your Plex media directly within Stremio.
      </p>
      <div className="mt-6">
        <Button onClick={handleLogin} className="w-full">
          Login
        </Button>
      </div>
    </div>
  );
};

export default Login;
