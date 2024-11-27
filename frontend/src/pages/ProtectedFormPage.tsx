import { FC } from 'react';
import FAQ from '@/components/faq.tsx';
import Header from '@/components/header.tsx';
import ProtectedForm from '@/components/protectedForm.tsx';
import { Toaster } from '@/components/ui/toaster.tsx';
import usePlexUser from '@/hooks/usePlexUser.tsx';

interface Props {
  plexToken: string | null;
  setPlexToken: (token: string | null) => void;
}

const ProtectedFormPage: FC<Props> = ({ plexToken, setPlexToken }) => {
  const plexUser = usePlexUser(plexToken);

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
