import React, { useState } from "react";

import NavBar from "../components/NavBar";
import { Upload } from "lucide-react";
import { UploadService } from "../services/UploadService";

function UploadPage() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [clauses, setClauses] = useState([]);

  const handleUpload = async (file) => {
    if (!file) return;
    try {
      const data = await UploadService(file);
      setClauses(data.clauses);
    } catch (error) {
      console.error("Error Uploading Contract:", error);
      throw error;
    }
  };
  return (
    <>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
        <NavBar />
        <div className="max-w-4xl mx-auto px-4 py-12">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Upload CDI Contract
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Upload your permanent employment contract (CDI) to automatically
              check its compliance with Moroccan Labor Law. We support PDF and
              DOCX formats.
            </p>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-8 mb-6">
            <div className="flex justify-center gap-4 flex-wrap">
              <div className="space-y-6 items-center text-center">
                <Upload className="w-16 h-16 text-green-500 mx-auto" />
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    click to browse
                  </h3>
                  <p className="text-gray-500 mb-4">
                    Supported formats: PDF, DOCX • Maximum size: 10MB
                  </p>

                  <label className="inline-flex items-center gap-2 px-8 py-3 bg-green-500 hover:bg-green-600 text-white rounded-lg cursor-pointer transition-colors font-medium shadow-lg hover:shadow-xl">
                    <Upload className="w-5 h-5" />
                    Choose File
                    <input
                      type="file"
                      className="hidden"
                      accept="application/pdf, application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                      onChange={(e) => handleUpload(e.target.files[0])}
                    />
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
        {/* Display Clauses*/}
        <div className="min-h-screen">
          <ul className="space-y-4">
            {clauses.map((clause) => (
              <li
                key={clause.index}
                className="rounded-2xl bg-white p-4 shadow-sm hover:shadow-md transition"
              >
                <strong className="text-gray-800">{clause.text}</strong>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </>
  );
}

export default UploadPage;
