import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { PageHeader, PageHeaderHeading } from "@/components/page-header";
import axios from 'axios';

interface Confession {
  id: number;
  confession: string;
  location: string;
}

function Feed() {
    const [confessions, setConfessions] = useState<Confession[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const baseUrl = import.meta.env.REACT_APP_API_URL;
        const apiUrl = `${baseUrl}/`;

        axios
            .get(apiUrl)
            .then((response) => {
                const confessionsArray: Confession[] = Object.values(response.data) as Confession[];
                confessionsArray.sort((a, b) => a.id - b.id);
                setConfessions(confessionsArray);
                setLoading(false);
            })
            .catch((error) => {
                console.error('Error fetching confessions', error);
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
                <div>
                    {confessions.map((confession: Confession, index: number) => (
                        <Card key={index} className="mb-3">
                            <CardHeader>
                                <CardTitle>Confession #{confession.id}</CardTitle>
                                <CardDescription>Location: {confession.location}</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <p>{confession.confession}</p>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}
        </>
    );
}

export default Feed;