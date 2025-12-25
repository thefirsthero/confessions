import { appConfig } from "@/config/app";

export function AppLogo() {
  return (
    <div className="flex items-center gap-2">
      <img src="/favicon.svg" alt="App Logo" className="size-6" />
      <span className="font-semibold text-nowrap">{appConfig.name}</span>
    </div>
  );
}
