type AppConfigType = {
  name: string;
  github: {
    title: string;
    url: string;
  };
  author: {
    name: string;
    url: string;
  };
  apiUrl: string;
};

export const appConfig: AppConfigType = {
  name: import.meta.env.VITE_APP_NAME ?? "Sample App",
  github: {
    title: "React Shadcn Starter",
    url: "https://github.com/thefirsthero/react-shadcn-starter",
  },
  author: {
    name: "thefirsthero",
    url: "https://github.com/thefirsthero/",
  },
  apiUrl: import.meta.env.VITE_API_URL ?? "http://localhost:8000",
};

export const baseUrl = import.meta.env.VITE_BASE_URL ?? "";
