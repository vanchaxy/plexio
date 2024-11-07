import ProtectedFormPage from "@/pages/ProtectedFormPage.tsx";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import AuthRedirectPage from "@/pages/AuthRedirectPage.tsx";
import usePlexToken from "@/hooks/usePlexToken.tsx";

function App() {
  const [token, setToken] = usePlexToken();

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/auth-redirect"
          element={<AuthRedirectPage setPlexToken={setToken} />}
        ></Route>
        <Route
          path="/*"
          element={
            <ProtectedFormPage plexToken={token} setPlexToken={setToken} />
          }
        ></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
