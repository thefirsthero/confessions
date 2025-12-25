import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { PageHeader, PageHeaderHeading } from "@/components/page-header";
import axios from "axios";
import { appConfig } from "@/config/app";

function Post() {
  const [confession, setConfession] = useState("");
  const [city, setCity] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [uploadSuccess, setUploadSuccess] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Clear any previous messages
    setUploadError(null);
    setUploadSuccess(null);

    // Append the specific endpoint
    const apiUrl = `${appConfig.apiUrl}/confessions`;
    const apiKey = import.meta.env.VITE_API_KEY;

    try {
      setIsUploading(true);

      const response = await axios.post(
        apiUrl,
        {
          id: -1,
          confession: String(confession),
          location: String(city),
        },
        {
          headers: apiKey ? { "X-API-Key": apiKey } : {},
        },
      );

      // Handle success, reset form, and display success message
      console.log("Submission successful", response);
      setConfession("");
      setCity("");
      setUploadSuccess("Confession added successfully");
    } catch (error) {
      // Handle errors, display error message, and reset uploading state
      console.error("Error submitting form", error);
      setUploadError("Error adding confession");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <>
      <PageHeader>
        <PageHeaderHeading>Make Your Confession</PageHeaderHeading>
      </PageHeader>
      <Card>
        <CardHeader>
          <CardTitle>What's on your mind?</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <div className="grid w-full items-center gap-4">
              <div className="flex flex-col space-y-1.5">
                <Textarea
                  id="confession"
                  placeholder="Enter your confession"
                  rows={5}
                  value={confession}
                  onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
                    setConfession(e.target.value)
                  }
                  required
                />
              </div>
              <div className="flex flex-col space-y-1.5">
                <Input
                  id="city"
                  type="text"
                  placeholder="Enter your location"
                  value={city}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    setCity(e.target.value)
                  }
                  required
                />
              </div>
            </div>
            <Button type="submit" disabled={isUploading} className="mt-4">
              {isUploading ? "Uploading..." : "Confess"}
            </Button>
          </form>
          {uploadError && <p className="text-red-500">{uploadError}</p>}
          {uploadSuccess && <p className="text-green-500">{uploadSuccess}</p>}
        </CardContent>
      </Card>
    </>
  );
}

export default Post;
