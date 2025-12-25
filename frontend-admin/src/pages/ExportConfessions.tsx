import { useState } from "react";
import { PageHeader, PageHeaderHeading } from "@/components/page-header";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { appConfig } from "@/config/app";
import axios from "axios";
import { Download, FileJson, Loader2 } from "lucide-react";

function ExportConfessions() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleExport = async () => {
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const apiKey = import.meta.env.VITE_API_KEY;
      const response = await axios.get(
        `${appConfig.apiUrl}/confessions/export`,
        {
          headers: apiKey ? { "X-API-Key": apiKey } : {},
          responseType: "blob",
        },
      );

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "MyConfessions.json");
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      setSuccess("MyConfessions.json downloaded successfully!");
    } catch (err) {
      console.error("Export error:", err);
      setError(
        err instanceof Error ? err.message : "Failed to export confessions",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <PageHeader>
        <PageHeaderHeading>Export Confessions</PageHeaderHeading>
      </PageHeader>

      <div className="max-w-2xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileJson className="h-5 w-5" />
              Generate MyConfessions.json
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm text-muted-foreground">
              Export all confessions from the database in video.json format for
              content generation. This includes the confession text, location,
              series information, and outro text.
            </p>

            <Button
              onClick={handleExport}
              disabled={loading}
              size="lg"
              className="w-full"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Exporting...
                </>
              ) : (
                <>
                  <Download className="mr-2 h-4 w-4" />
                  Download MyConfessions.json
                </>
              )}
            </Button>

            {error && (
              <div className="text-sm text-destructive bg-destructive/10 px-3 py-2 rounded-md">
                {error}
              </div>
            )}

            {success && (
              <div className="text-sm text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-950 px-3 py-2 rounded-md">
                {success}
              </div>
            )}

            <div className="pt-4 border-t">
              <h3 className="text-sm font-medium mb-2">Output Format:</h3>
              <pre className="text-xs bg-muted p-3 rounded-md overflow-x-auto">
                {JSON.stringify(
                  [
                    {
                      series: "Your Confessions",
                      part: "1",
                      outro: "Visit confess.coraxi.com to anonymously confess",
                      text: "Confession text with location appended.",
                    },
                  ],
                  null,
                  2,
                )}
              </pre>
            </div>
          </CardContent>
        </Card>
      </div>
    </>
  );
}

export default ExportConfessions;
