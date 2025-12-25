import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

interface Confession {
  id: number;
  confession: string;
  location: string;
}

interface ConfessionCardProps {
  confession: Confession;
}

const cardHighlightColors = [
  "border-red-500",
  "border-blue-500",
  "border-green-500",
  "border-yellow-500",
  "border-purple-500",
  "border-pink-500",
  "border-indigo-500",
  "border-gray-500",
];

export function ConfessionCard({ confession }: ConfessionCardProps) {
  const [highlightColor, setHighlightColor] = useState("");

  useEffect(() => {
    const randomColor = cardHighlightColors[Math.floor(Math.random() * cardHighlightColors.length)];
    setHighlightColor(randomColor);
  }, []);

  return (
    <Card className="break-inside-avoid-column mb-4">
      <CardHeader className={`border-l-4 ${highlightColor}`}>
        <CardTitle>Confession #{confession.id}</CardTitle>
        <CardDescription>Location: {confession.location}</CardDescription>
      </CardHeader>
      <CardContent>
        <p>{confession.confession}</p>
      </CardContent>
    </Card>
  );
}
