import usePlexUser from "@/hooks/usePlexUser.tsx";
import Login from "@/components/login.tsx";
import Loading from "@/components/loading.tsx";
import ConfigurationForm from "@/components/configurationForm.tsx";
import { FC } from "react";

interface Props {
  plexToken: string;
  setPlexToken: (token: string | null) => void;
}

const ProtectedFormPage: FC<Props> = ({ plexToken, setPlexToken }) => {
  const plexUser = usePlexUser(plexToken);

  if (plexUser === undefined) {
    return <Loading />;
  }
  if (plexUser === null) {
    return <Login />;
  }
  return (
    <ConfigurationForm
      plexToken={plexToken}
      setPlexToken={setPlexToken}
      plexUser={plexUser}
    />
  );
};

export default ProtectedFormPage;
