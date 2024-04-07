import { Button } from "@/components/ui/button"
import { ThemeProvider } from "@/components/theme-provider"
import {ModeToggle} from "@/components/mode-toggle.tsx";

function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <ModeToggle />
      <Button variant="outline">Button</Button>
    </ThemeProvider>
  )
}

export default App
