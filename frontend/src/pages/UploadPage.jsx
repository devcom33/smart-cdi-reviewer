import React, { useState } from "react";

import NavBar from "../components/NavBar";
import { Upload } from "lucide-react";

function UploadPage() {
  const [isProcessing, setIsProcessing] = useState(false);
  const handleUpload = async (file) => {
    if (!file) return;
  };
  return (
    <>
      <NavBar />
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="flex justify-center gap-4 flex-wrap">
          <label className="flex items-center gap-2 px-6 py-3 bg-green-400 hover:bg-green-500 text-white rounded-lg cursor-pointer transition-colors font-medium">
            <Upload className="w-5 h-5" />
            Upload
            <input
              type="file"
              className="hidden"
              accept="application/pdf, application/vnd.openxmlformats-officedocument.wordprocessingml.document"
              onChange={(e) => handleUpload(e.target.files[0])}
            />
          </label>
        </div>
      </div>
    </>
  );
}

export default UploadPage;
