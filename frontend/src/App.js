import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "@/components/Layout";
import HomePage from "@/pages/HomePage";
import UploadPage from "@/pages/UploadPage";
import AskPage from "@/pages/AskPage";
import StatusPage from "@/pages/StatusPage";

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/ask" element={<AskPage />} />
          <Route path="/status" element={<StatusPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
