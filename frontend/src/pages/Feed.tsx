import { useState, useEffect } from "react";
import { PageHeader, PageHeaderHeading } from "@/components/page-header";
import axios from "axios";
import { appConfig } from "@/config/app";
import { ConfessionCard } from "@/components/confession-card";

interface Confession {
  id: number;
  confession: string;
  location: string;
}

function Feed() {
  const [confessions, setConfessions] = useState<Confession[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const apiUrl = `${appConfig.apiUrl}/confessions`;
    const apiKey = import.meta.env.VITE_API_KEY;

    axios
      .get(apiUrl, {
        headers: apiKey ? { "X-API-Key": apiKey } : {},
      })
      .then((response) => {
        const confessionsArray: Confession[] = Object.values(
          response.data,
        ) as Confession[];
        confessionsArray.sort((a, b) => a.id - b.id);
        setConfessions(confessionsArray);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching confessions", error);
        setLoading(false);
      });
  }, []);

  return (
    <>
      <PageHeader>
        <PageHeaderHeading>Confessions Feed</PageHeaderHeading>
      </PageHeader>
      {loading && <p className="loading-message">Loading confessions...</p>}

      {!loading && confessions.length === 0 && (
        <p className="no-confessions-message">No confessions available.</p>
      )}

      {!loading && confessions.length > 0 && (
        <div className="columns-1 sm:columns-2 lg:columns-3 gap-4">
          {confessions.map((confession: Confession) => (
            <ConfessionCard key={confession.id} confession={confession} />
          ))}
        </div>
      )}
    </>
  );
}

export default Feed;
