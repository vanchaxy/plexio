import { FC } from 'react';
import { UseFormReturn } from 'react-hook-form';
import { ConfigurationFormType } from '@/components/configurationForm/formSchema.tsx';
import { Checkbox } from '@/components/ui/checkbox.tsx';
import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form.tsx';
import { Switch } from '@/components/ui/switch.tsx';

const transcodeDownQualities = ['1080p', '720p', '480p'];

interface Props {
  form: UseFormReturn<ConfigurationFormType>;
}

export const IncludeTranscodeDownFields: FC<Props> = ({ form }) => {
  const includeTranscodeDown = form.watch('includeTranscodeDown');

  return (
    <>
      <FormField
        control={form.control}
        name="includeTranscodeDown"
        render={({ field }) => (
          <FormItem className="items-center justify-between flex flex-row rounded-lg border p-2">
            <div className="space-y-0.5">
              <FormLabel className="text-base">
                Include Transcoded Streams with Lower Resolutions
              </FormLabel>
              <FormDescription>
                Include transcoded streams with lower qualities.
              </FormDescription>
            </div>
            <FormControl>
              <Switch checked={field.value} onCheckedChange={field.onChange} />
            </FormControl>
          </FormItem>
        )}
      />

      {includeTranscodeDown && (
        <FormField
          control={form.control}
          name="transcodeDownQualities"
          render={() => (
            <FormItem className="rounded-lg border p-2">
              <div className="mb-4">
                <FormLabel className="text-base">Lower Resolutions</FormLabel>
                <FormDescription>
                  Select transcoding resolutions to include.
                </FormDescription>
              </div>
              {transcodeDownQualities.map((item) => (
                <FormField
                  key={item}
                  control={form.control}
                  name="transcodeDownQualities"
                  render={({ field }) => {
                    return (
                      <FormItem
                        key={item}
                        className="flex flex-row items-start space-x-3 space-y-0"
                      >
                        <FormControl>
                          <Checkbox
                            checked={field.value?.includes(item)}
                            onCheckedChange={(checked) => {
                              return checked
                                ? field.onChange([...(field.value || []), item])
                                : field.onChange(
                                    field.value?.filter(
                                      (value) => value !== item,
                                    ),
                                  );
                            }}
                          />
                        </FormControl>
                        <FormLabel className="font-normal">{item}</FormLabel>
                      </FormItem>
                    );
                  }}
                />
              ))}
              <FormMessage />
            </FormItem>
          )}
        />
      )}
    </>
  );
};
