import { Image, FileJson, LucideIcon } from "lucide-react";

type MenuItemType = {
  title: string;
  url: string;
  external?: string;
  icon?: LucideIcon;
  items?: MenuItemType[];
};
type MenuType = MenuItemType[];

export const mainMenu: MenuType = [
  {
    title: "Process Images",
    url: "/process",
    icon: Image,
  },
  {
    title: "Export Confessions",
    url: "/export",
    icon: FileJson,
  },
];
