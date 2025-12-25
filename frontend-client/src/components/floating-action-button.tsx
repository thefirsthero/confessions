import { Link } from "react-router-dom";
import { Button } from "./ui/button";
import { Plus } from "lucide-react";

export function FloatingActionButton() {
  return (
    <div className="fixed bottom-4 right-4">
      <Link to="/post">
        <Button className="rounded-full w-16 h-16 shadow-lg">
          <Plus className="w-8 h-8" />
        </Button>
      </Link>
    </div>
  );
}
