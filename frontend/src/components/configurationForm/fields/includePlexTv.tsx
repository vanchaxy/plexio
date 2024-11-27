import { FC } from 'react';
import { UseFormReturn } from 'react-hook-form';
import { ConfigurationFormType } from '@/components/configurationForm/formSchema.tsx';
import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
} from '@/components/ui/form.tsx';
import { Switch } from '@/components/ui/switch.tsx';

interface Props {
  form: UseFormReturn<ConfigurationFormType>;
}

export const IncludePlexTvField: FC<Props> = ({ form }) => {
  return (
    <FormField
      control={form.control}
      name="includePlexTv"
      render={({ field }) => (
        <FormItem className="items-center justify-between flex flex-row rounded-lg border p-2">
          <div className="space-y-0.5">
            <FormLabel className="text-base">Include Plex.tv URL</FormLabel>
            <FormDescription>
              Include a stream redirecting to the Plex app or website.
            </FormDescription>
          </div>
          <FormControl>
            <Switch checked={field.value} onCheckedChange={field.onChange} />
          </FormControl>
        </FormItem>
      )}
    />
  );
};
