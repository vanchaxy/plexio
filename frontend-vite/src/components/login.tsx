import { Button } from "@/components/ui/button.tsx";
import useClientIdentifier from "@/hooks/useClientIdentifier.tsx";
import { createAuthPin } from "@/services/PlexService.tsx";

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

  return <Button onClick={handleLogin}> Login </Button>;
};

export default Login;
