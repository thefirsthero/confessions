import { Button } from "@/components/ui/button";
import { appConfig } from "@/config/app";
import { LogOut } from "lucide-react";
import { useNavigate } from "react-router-dom";

export function AppNavbar() {
  const navigate = useNavigate();

  const openTikTokPage = () => {
    window.open(appConfig.tiktok.url, "_blank");
  };

  const handleLogout = () => {
    localStorage.removeItem("auth_token");
    navigate("/login");
  };

  return (
    <div className="flex items-center space-x-2">
      <Button variant="ghost" onClick={openTikTokPage}>
        <img src="/tiktok-logo.svg" alt="TikTok Logo" className="h-6 w-6" />
        <span className="hidden sm:inline">TikTok</span>
      </Button>
      <Button variant="ghost" onClick={handleLogout}>
        <LogOut className="h-4 w-4" />
        <span className="hidden sm:inline">Logout</span>
      </Button>
    </div>
  );
}
