import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion.tsx';

const QUESTIONS = [
  {
    id: 'what-is-plexio',
    question: `What is Plexio?`,
    answer: `Plexio is a Stremio addon that allows you to integrate your Plex library into Stremio.`,
  },
];

const FAQ = () => {
  return (
    <div className="mt-5 mb-5 border rounded-lg p-6">
      <h2 className="text-md font-semibold">Frequently Asked Questions</h2>
      <Accordion type="multiple" className="mt-4">
        {QUESTIONS.map((item) => (
          <AccordionItem value={item.id} key={item.id}>
            <AccordionTrigger>{item.question}</AccordionTrigger>
            <AccordionContent>{item.answer}</AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    </div>
  );
};

export default FAQ;
