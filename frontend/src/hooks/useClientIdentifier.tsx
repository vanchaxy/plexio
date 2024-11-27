import { useEffect, useState } from 'react';
import { v4 as uuidv4 } from 'uuid';

const useClientIdentifier = (): string => {
  const [clientIdentifier, setClientIdentifier] = useState<string>('');

  useEffect(() => {
    const storedClientIdentifier = localStorage.getItem('clientIdentifier');

    if (storedClientIdentifier) {
      setClientIdentifier(storedClientIdentifier);
    } else {
      const newClientIdentifier = uuidv4();
      localStorage.setItem('clientIdentifier', newClientIdentifier);
      setClientIdentifier(newClientIdentifier);
    }
  }, []);

  return clientIdentifier;
};

export default useClientIdentifier;
