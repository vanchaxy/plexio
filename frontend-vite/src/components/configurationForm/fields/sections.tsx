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

interface Props {
  form: UseFormReturn<ConfigurationFormType>;
  sections: any[];
}

export const SectionsField: FC<Props> = ({ form, sections }) => {
  return (
    <FormField
      control={form.control}
      name="sections"
      render={() => (
        <FormItem className="rounded-lg border p-2">
          <div className="mb-4">
            <FormLabel className="text-base">Sections</FormLabel>
            <FormDescription>
              Select the Plex library sections to access in Stremio.
            </FormDescription>
          </div>
          {sections.length > 0 ? (
            sections.map((item: any) => (
              <FormField
                key={item.key}
                control={form.control}
                name="sections"
                render={({ field }) => {
                  return (
                    <FormItem
                      key={item.key}
                      className="flex flex-row items-start space-x-3 space-y-0"
                    >
                      <FormControl>
                        <Checkbox
                          checked={field.value?.some((v) => v.key === item.key)}
                          onCheckedChange={(checked) => {
                            return checked
                              ? field.onChange([
                                  ...(field.value || []),
                                  {
                                    key: item.key,
                                    title: item.title,
                                    type: item.type,
                                  },
                                ])
                              : field.onChange(
                                  field.value?.filter(
                                    (value) => value.key !== item.key,
                                  ),
                                );
                          }}
                        />
                      </FormControl>
                      <FormLabel className="font-normal">
                        {item.title}
                      </FormLabel>
                    </FormItem>
                  );
                }}
              />
            ))
          ) : (
            <div className="flex flex-col items-center justify-center">
              <div className="w-16 h-16 rounded-full animate-spin border-t-4 border-muted-foreground" />
              <span className="mt-4 text-lg text-muted-foreground text-center">
                Loading sections from the server using the selected discovery
                URL.
                <br />
                If this takes too long, try selecting a different discovery URL.
              </span>
            </div>
          )}
          <FormMessage />
        </FormItem>
      )}
    />
  );
};
