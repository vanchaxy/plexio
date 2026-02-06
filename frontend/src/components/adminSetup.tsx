import { FormEvent, useState } from 'react';
import { Button } from '@/components/ui/button.tsx';
import { Label } from '@/components/ui/label.tsx';

interface Props {
  onSetup: (username: string, password: string) => Promise<{
    success: boolean;
    error?: string;
  }>;
}

const AdminSetup = ({ onSetup }: Props) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setIsSubmitting(true);
    const result = await onSetup(username.trim(), password);
    setIsSubmitting(false);

    if (!result.success) {
      setError(result.error ?? 'Unable to set admin credentials.');
    }
  };

  return (
    <div className="border rounded-lg p-6">
      <h1 className="text-xl font-bold text-center">Admin Setup</h1>
      <p className="text-sm text-center mt-2 text-muted-foreground">
        Create the admin username and password to secure Plexio on first run.
      </p>
      <form
        className="mt-6 space-y-4"
        onSubmit={(event) => void handleSubmit(event)}
      >
        <div className="space-y-2">
          <Label htmlFor="admin-username">Admin username</Label>
          <input
            id="admin-username"
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            placeholder="Enter a username"
            required
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="admin-password">Admin password</Label>
          <input
            id="admin-password"
            type="password"
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Create a password"
            required
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="admin-password-confirm">Confirm password</Label>
          <input
            id="admin-password-confirm"
            type="password"
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            value={confirmPassword}
            onChange={(event) => setConfirmPassword(event.target.value)}
            placeholder="Repeat the password"
            required
          />
        </div>
        {error && <p className="text-sm text-destructive">{error}</p>}
        <Button className="w-full" type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Saving…' : 'Save admin credentials'}
        </Button>
      </form>
    </div>
  );
};

export default AdminSetup;
