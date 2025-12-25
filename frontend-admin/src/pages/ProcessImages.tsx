import { useState, useRef } from "react";
import { PageHeader, PageHeaderHeading } from "@/components/page-header";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { appConfig } from "@/config/app";
import axios from "axios";
import {
  Upload,
  Image as ImageIcon,
  FileJson,
  Loader2,
  X,
  Download,
  CheckCircle2,
} from "lucide-react";

interface ProcessedConfession {
  series: string;
  part: string;
  outro: string;
  text: string;
}

function ProcessImages() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ProcessedConfession[] | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = Array.from(e.target.files);
      setSelectedFiles((prev) => [...prev, ...files]);
      setError(null);
    }
  };

  const removeFile = (index: number) => {
    setSelectedFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleProcess = async () => {
    if (selectedFiles.length === 0) {
      setError("Please select at least one image");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      selectedFiles.forEach((file) => {
        formData.append("images", file);
      });

      const apiKey = import.meta.env.VITE_API_KEY;
      const response = await axios.post<ProcessedConfession[]>(
        `${appConfig.apiUrl}/images/process`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            ...(apiKey ? { "X-API-Key": apiKey } : {}),
          },
        },
      );

      setResult(response.data);
    } catch (err) {
      console.error("Processing error:", err);
      setError(err instanceof Error ? err.message : "Failed to process images");
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadJson = () => {
    if (!result) return;

    const blob = new Blob([JSON.stringify(result, null, 2)], {
      type: "application/json",
    });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "video.json");
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  };

  const handleReset = () => {
    setSelectedFiles([]);
    setResult(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <>
      <PageHeader>
        <PageHeaderHeading>Process Images</PageHeaderHeading>
      </PageHeader>

      <div className="max-w-4xl mx-auto space-y-6">
        {/* Upload Section */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ImageIcon className="h-5 w-5" />
              Upload Confession Images
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm text-muted-foreground">
              Upload confession images for OCR processing. The system will
              extract text, clean it, and generate a video.json file for content
              creation.
            </p>

            <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-8 text-center hover:border-muted-foreground/50 transition-colors">
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                multiple
                onChange={handleFileSelect}
                className="hidden"
                id="image-upload"
              />
              <label
                htmlFor="image-upload"
                className="cursor-pointer flex flex-col items-center gap-2"
              >
                <Upload className="h-10 w-10 text-muted-foreground" />
                <span className="text-sm font-medium">
                  Click to upload images
                </span>
                <span className="text-xs text-muted-foreground">
                  PNG, JPG, JPEG supported
                </span>
              </label>
            </div>

            {/* Selected Files */}
            {selectedFiles.length > 0 && (
              <div className="space-y-2">
                <h3 className="text-sm font-medium">
                  Selected Images ({selectedFiles.length})
                </h3>
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {selectedFiles.map((file, index) => (
                    <div
                      key={index}
                      className="flex items-center gap-2 p-2 bg-muted rounded-md"
                    >
                      <ImageIcon className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                      <span className="text-sm flex-1 truncate">
                        {file.name}
                      </span>
                      <span className="text-xs text-muted-foreground">
                        {(file.size / 1024).toFixed(1)} KB
                      </span>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeFile(index)}
                        className="h-6 w-6 p-0"
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="flex gap-2">
              <Button
                onClick={handleProcess}
                disabled={loading || selectedFiles.length === 0}
                size="lg"
                className="flex-1"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Processing {selectedFiles.length} image(s)...
                  </>
                ) : (
                  <>
                    <FileJson className="mr-2 h-4 w-4" />
                    Process Images
                  </>
                )}
              </Button>

              {selectedFiles.length > 0 && !loading && (
                <Button onClick={handleReset} variant="outline" size="lg">
                  Reset
                </Button>
              )}
            </div>

            {error && (
              <div className="text-sm text-destructive bg-destructive/10 px-3 py-2 rounded-md">
                {error}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Results Section */}
        {result && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle2 className="h-5 w-5 text-green-600" />
                Processing Complete
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <p className="text-sm text-muted-foreground">
                  Successfully processed {result.length} confession(s)
                </p>
                <Button onClick={handleDownloadJson} size="sm">
                  <Download className="mr-2 h-4 w-4" />
                  Download video.json
                </Button>
              </div>

              <div className="space-y-3 max-h-96 overflow-y-auto">
                {result.map((confession, index) => (
                  <Card key={index} className="bg-muted/50">
                    <CardContent className="pt-4 space-y-2">
                      <div className="flex items-center gap-2 text-sm font-medium">
                        <span className="text-muted-foreground">
                          Confession #{confession.part}
                        </span>
                        <span className="text-xs px-2 py-1 bg-background rounded-md">
                          {confession.series}
                        </span>
                      </div>
                      <p className="text-sm">{confession.text}</p>
                      <p className="text-xs text-muted-foreground italic">
                        {confession.outro}
                      </p>
                    </CardContent>
                  </Card>
                ))}
              </div>

              <div className="pt-4 border-t">
                <h3 className="text-sm font-medium mb-2">JSON Output:</h3>
                <pre className="text-xs bg-background p-3 rounded-md overflow-x-auto max-h-48">
                  {JSON.stringify(result, null, 2)}
                </pre>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </>
  );
}

export default ProcessImages;
