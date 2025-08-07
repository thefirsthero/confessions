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
  tiktok: {
    url: string;
  };
};

export const appConfig: AppConfigType = {
  name: import.meta.env.VITE_APP_NAME ?? "Sample App",
  github: {
    title: "Confessions",
    url: "https://github.com/thefirsthero/confessions",
  },
  author: {
    name: "thefirsthero",
    url: "https://github.com/thefirsthero/",
  },
  apiUrl: import.meta.env.VITE_API_URL ?? "http://localhost:8000",
  tiktok: {
    url: "https://www.tiktok.com/@zaconfessions",
  },
};

export const baseUrl = import.meta.env.VITE_BASE_URL ?? "";
