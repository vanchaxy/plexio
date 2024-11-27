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
    answer: `Plexio allows you to integrate your Plex library with Streamio, enabling seamless access to your media.`,
  },
  {
    id: 'is-free',
    question: `Is Plexio free?`,
    answer: `Yes, Plexio is free to use with your existing Plex and Streamio accounts.`,
  },
  {
    id: 'how-to-connect',
    question: `How do I connect Plex to Streamio?`,
    answer: `Simply log in using your Plex account, and Plexio will handle the integration with Streamio.`,
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
