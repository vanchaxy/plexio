import { FC } from 'react';
import AdminLogin from '@/components/adminLogin.tsx';
import AdminSetup from '@/components/adminSetup.tsx';
import FAQ from '@/components/faq.tsx';
import Header from '@/components/header.tsx';
import ProtectedForm from '@/components/protectedForm.tsx';
import { Toaster } from '@/components/ui/toaster.tsx';
import useAdminAuth from '@/hooks/useAdminAuth.tsx';
import usePlexUser from '@/hooks/usePlexUser.tsx';

interface Props {
  plexToken: string | null;
  setPlexToken: (token: string | null) => void;
}

const ProtectedFormPage: FC<Props> = ({ plexToken, setPlexToken }) => {
  const {
    adminConfig,
    adminUsername,
    authenticate,
    configureAdmin,
    isAuthenticated,
  } = useAdminAuth();
  const plexUser = usePlexUser(plexToken);

  if (!adminConfig) {
    return (
      <div className="mx-auto max-w-2xl">
        <Toaster />
        <AdminSetup onSetup={configureAdmin} />
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="mx-auto max-w-2xl">
        <Toaster />
        <AdminLogin adminUsername={adminUsername} onLogin={authenticate} />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-2xl">
      <Toaster />
      <Header plexUser={plexUser} setPlexToken={setPlexToken}></Header>
      <ProtectedForm plexToken={plexToken} plexUser={plexUser} />
      <FAQ />
    </div>
  );
};

export default ProtectedFormPage;
