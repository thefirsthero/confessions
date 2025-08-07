import { Link, NavLink } from "react-router-dom";
import { mainMenu } from "@/config/menu";
import { cn } from "@/lib/utils";
import { AppLogo } from "./app-logo";
import { AppSidebar } from "./app-sidebar";

export function AppHeader() {
  return (
    <header className="bg-background sticky top-0 z-50 border-b">
      <div className="w-full ~max-w-7xl mx-auto flex items-center gap-2 h-14 px-4 md:px-8">
        <div className="flex items-center gap-2 md:gap-0">
          <AppSidebar />
          <Link to="/">
            <AppLogo />
          </Link>
        </div>

        <div className="ml-4 flex-1 flex items-center justify-between">
          <div className="flex-1">
            <nav className="hidden md:flex gap-1">
              {mainMenu.map((item, index) => (
                <NavLink
                  key={index}
                  to={item.url}
                  className={({ isActive }) =>
                    cn(
                      "flex items-center gap-2 overflow-hidden rounded-md p-2.5 text-left text-sm outline-none transition-[width,height,padding] hover:bg-accent hover:text-accent-foreground focus-visible:ring-2 active:bg-accent active:text-accent-foreground disabled:pointer-events-none disabled:opacity-50 aria-disabled:pointer-events-none aria-disabled:opacity-50 [&>svg]:size-4",
                      "h-8 text-sm hover:bg-accent hover:text-accent-foreground",
                      isActive
                        ? "text-foreground bg-accent"
                        : "text-foreground/70",
                    )
                  }
                >
                  {item.icon && <item.icon />}
                  <span className="font-medium">{item.title}</span>
                </NavLink>
              ))}
            </nav>
          </div>
          <nav className="flex gap-1">
          </nav>
        </div>
      </div>
    </header>
  );
}
