import { FormEvent, useState } from 'react';
import { Button } from '@/components/ui/button.tsx';
import { Label } from '@/components/ui/label.tsx';

interface Props {
  adminUsername: string | null;
  onLogin: (username: string, password: string) => Promise<{
    success: boolean;
    error?: string;
  }>;
}

const AdminLogin = ({ adminUsername, onLogin }: Props) => {
  const [username, setUsername] = useState(adminUsername ?? '');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);

    setIsSubmitting(true);
    const result = await onLogin(username.trim(), password);
    setIsSubmitting(false);

    if (!result.success) {
      setError(result.error ?? 'Unable to sign in.');
    }
  };

  return (
    <div className="border rounded-lg p-6">
      <h1 className="text-xl font-bold text-center">Admin Login</h1>
      <p className="text-sm text-center mt-2 text-muted-foreground">
        Sign in with the admin credentials to access Plexio configuration.
      </p>
      <form
        className="mt-6 space-y-4"
        onSubmit={(event) => void handleSubmit(event)}
      >
        <div className="space-y-2">
          <Label htmlFor="admin-login-username">Admin username</Label>
          <input
            id="admin-login-username"
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            placeholder="Enter your username"
            required
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="admin-login-password">Admin password</Label>
          <input
            id="admin-login-password"
            type="password"
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Enter your password"
            required
          />
        </div>
        {error && <p className="text-sm text-destructive">{error}</p>}
        <Button className="w-full" type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Signing in…' : 'Sign in'}
        </Button>
      </form>
    </div>
  );
};

export default AdminLogin;
