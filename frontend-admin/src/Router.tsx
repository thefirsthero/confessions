import { Routes, Route } from "react-router-dom";
import { AppLayout } from "./components/app-layout";
import ExportConfessions from "./pages/ExportConfessions";
import ProcessImages from "./pages/ProcessImages";
import Login from "./pages/Login";
import ProtectedRoute from "./components/ProtectedRoute";

export default function Router() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/" element={<ProcessImages />} />
        <Route path="/process" element={<ProcessImages />} />
        <Route path="/export" element={<ExportConfessions />} />
        <Route path="*" element={<ProcessImages />} />
      </Route>
    </Routes>
  );
}
