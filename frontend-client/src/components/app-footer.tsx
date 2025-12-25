import { appConfig } from "@/config/app";
import { ModeToggle } from "./mode-toggle";

export function AppFooter() {
  return (
    <footer className="flex flex-col items-center justify-between gap-4 min-h-[3rem] md:h-20 py-2 md:flex-row">
      <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
        Like this platform?{" "}
        <a
          href={appConfig.buyMeACoffeeUrl}
          target="_blank"
          rel="noreferrer"
          className="font-medium underline underline-offset-4"
        >
          Buy Me A Coffee
        </a>
        .
      </p>
      <div className="hidden md:block">
        <ModeToggle />
      </div>
    </footer>
  );
}
