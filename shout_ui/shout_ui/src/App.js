import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/Home";
import { Dashboard } from "./layouts/dashboard";
import Registration from "./pages/Registration";


function App() {
  return (
    <Routes>
      <Route exact path="/" element={<HomePage />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/register" element={<Registration />} />
    </Routes>
  );
}

export default App;
