import { Routes, Route } from "react-router-dom";
import { AppLayout } from "./components/app-layout";
import Feed from "./pages/Feed";
import Post from "./pages/Post";

export default function Router() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<Feed />} />
        <Route path="/make-confession" element={<Post />} />
        {/* Keep a catch-all for now, can be simplified later if needed */}
        <Route path="*" element={<Feed />} /> 
      </Route>
    </Routes>
  );
}
