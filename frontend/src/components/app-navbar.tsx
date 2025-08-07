
import { Button } from "@/components/ui/button";

export function AppNavbar() {
  const openTikTokPage = () => {
    window.open("https://www.tiktok.com/@zaconfessions", "_blank");
  };

  return (
    <div className="flex items-center space-x-2">
      <Button variant="ghost" onClick={openTikTokPage}>
        <img src="/tiktok-logo.svg" alt="TikTok Logo" className="h-6 w-6" />
        <span>TikTok</span>
      </Button>
    </div>
  );
}
