import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

interface Confession {
  id: number;
  confession: string;
  location: string;
}

interface ConfessionCardProps {
  confession: Confession;
}

export function ConfessionCard({ confession }: ConfessionCardProps) {
  return (
    <Card className="break-inside-avoid-column mb-4">
      <CardHeader>
        <CardTitle>Confession #{confession.id}</CardTitle>
        <CardDescription>Location: {confession.location}</CardDescription>
      </CardHeader>
      <CardContent>
        <p>{confession.confession}</p>
      </CardContent>
    </Card>
  );
}
