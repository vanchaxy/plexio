import { FC } from 'react';
import { UseFormReturn } from 'react-hook-form';
import { ConfigurationFormType } from '@/components/configurationForm/formSchema.tsx';
import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form.tsx';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select.tsx';

interface Props {
  form: UseFormReturn<ConfigurationFormType>;
  servers: PlexServer[];
}

export const ServerNameField: FC<Props> = ({ form, servers }) => {
  return (
    <FormField
      control={form.control}
      name="serverName"
      render={({ field }) => (
        <FormItem className="rounded-lg border p-2">
          <FormLabel className="text-base">Plex Server</FormLabel>
          <Select
            onValueChange={(s) => {
              form.resetField('discoveryUrl', { defaultValue: '' });
              form.resetField('streamingUrl', { defaultValue: '' });
              form.resetField('sections', { defaultValue: [] });
              field.onChange(s);
            }}
            defaultValue={field.value}
          >
            <FormControl>
              <SelectTrigger>
                <SelectValue placeholder="Select a server name" />
              </SelectTrigger>
            </FormControl>
            <SelectContent>
              {servers.map((s, index) => (
                <SelectItem key={index} value={s.name}>
                  {s.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <FormDescription>Choose your Plex server.</FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  );
};
