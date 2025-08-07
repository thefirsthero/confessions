import { NavLink } from "react-router-dom";
import { Button } from "@/components/ui/button";

export function AppNavbar() {
  const openTikTokPage = () => {
    window.open("https://www.tiktok.com/@zaconfessions", "_blank");
  };

  return (
    <div className="flex items-center space-x-2">
      <Button variant="ghost" onClick={openTikTokPage}>
        {/* Add a TikTok icon here */}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="lucide lucide-tiktok"
        >
          <path d="M12 12a4 4 0 1 0 4 4V8a4 4 0 1 0-4 4h4" />
          <path d="M12 12v8" />
        </svg>
      </Button>
      <Button asChild variant="ghost">
        <NavLink to="/make-confession">Make Confession</NavLink>
      </Button>
      <Button asChild variant="ghost">
        <NavLink to="/feed">Feed</NavLink>
      </Button>
    </div>
  );
}
