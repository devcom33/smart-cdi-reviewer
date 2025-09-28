import React, { useState } from "react";
import NavBar from "../components/NavBar";
import {
  Upload,
  X,
  CheckCircle,
  AlertCircle,
  FileText,
  Loader2,
} from "lucide-react";
import { UploadService } from "../services/UploadService";
import { ResultService } from "../services/ResultService";

function UploadPage() {
  const [clauses, setClauses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [fileName, setFileName] = useState("");

  const pollResult = async (id) => {
    let delay = 2000;
    const maxDelay = 60000;
    const maxTime = 5 * 60 * 1000;
    let elapsed = 0;

    while (elapsed < maxTime) {
      const result = await ResultService(id);
      if (result.status === "ok") {
        setClauses(result.output);
        setLoading(false);
        setShowModal(true);
        return;
      }
      await new Promise((r) => setTimeout(r, delay));
      elapsed += delay;
      delay = Math.min(delay * 2, maxDelay);
    }
    setLoading(false);
    alert("Result not ready after 5 minutes. Please try again later.");
  };

  const handleUpload = async (file) => {
    if (!file) return;
    try {
      setFileName(file.name);
      setLoading(true);
      const { id } = await UploadService(file);
      if (id) {
        pollResult(id);
      } else {
        console.error("Id not found");
        setLoading(false);
      }
    } catch (error) {
      console.error("Error Uploading Contract:", error);
      setLoading(false);
    }
  };

  const closeModal = () => {
    setShowModal(false);
    setClauses([]);
    setFileName("");
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
            <div className="flex justify-center">
              <div className="space-y-6 items-center text-center">
                {loading ? (
                  <div className="flex flex-col items-center space-y-4">
                    <Loader2 className="w-16 h-16 text-green-500 animate-spin" />
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-2">
                        Processing {fileName}...
                      </h3>
                      <p className="text-gray-500">
                        Analyzing your contract for compliance issues
                      </p>
                    </div>
                  </div>
                ) : (
                  <>
                    <Upload className="w-16 h-16 text-green-500 mx-auto" />
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-2">
                        Click to browse
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
                  </>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Results Modal */}
        {showModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-xl shadow-2xl w-full max-w-4xl max-h-[90vh] flex flex-col">
              {/* Modal Header */}
              <div className="flex items-center justify-between p-6 border-b border-gray-200">
                <div className="flex items-center gap-3">
                  <FileText className="w-6 h-6 text-green-500" />
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900">
                      Contract Analysis Results
                    </h3>
                    <p className="text-sm text-gray-500">{fileName}</p>
                  </div>
                </div>
                <button
                  onClick={closeModal}
                  className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <X className="w-5 h-5 text-gray-500" />
                </button>
              </div>

              {/* Modal Body */}
              <div className="flex-1 overflow-y-auto p-6">
                {clauses.length === 0 ? (
                  <div className="text-center py-8">
                    <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
                    <h4 className="text-lg font-semibold text-gray-900 mb-2">
                      No Issues Found
                    </h4>
                    <p className="text-gray-600">
                      Your contract appears to be compliant with Moroccan Labor
                      Law.
                    </p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {clauses.map((clause, index) => (
                      <div
                        key={clause.clause_index || index}
                        className="bg-gray-50 rounded-lg p-5 border border-gray-200"
                      >
                        <div className="flex items-start gap-3 mb-3">
                          <AlertCircle className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
                          <div className="flex-1">
                            <h4 className="font-semibold text-gray-900 mb-2">
                              Clause {clause.clause_index || index + 1}
                            </h4>
                            <p className="text-gray-700 mb-3 leading-relaxed">
                              {clause.clause_text}
                            </p>
                          </div>
                        </div>

                        {clause.issue && (
                          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-3">
                            <div className="flex items-start gap-2">
                              <AlertCircle className="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0" />
                              <div>
                                <h5 className="font-medium text-red-800 mb-1">
                                  Issue Identified
                                </h5>
                                <p className="text-red-700 text-sm">
                                  {clause.issue}
                                </p>
                              </div>
                            </div>
                          </div>
                        )}

                        {clause.suggestion && (
                          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                            <div className="flex items-start gap-2">
                              <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                              <div>
                                <h5 className="font-medium text-green-800 mb-1">
                                  Suggested Fix
                                </h5>
                                <p className="text-green-700 text-sm">
                                  {clause.suggestion}
                                </p>
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Modal Footer */}
              <div className="border-t border-gray-200 p-6 bg-gray-50 rounded-b-xl">
                <div className="flex justify-between items-center">
                  <p className="text-sm text-gray-600">
                    {clauses.length > 0
                      ? `Found ${clauses.length} clause${
                          clauses.length !== 1 ? "s" : ""
                        } that need attention`
                      : "Contract analysis complete"}
                  </p>
                  <div className="flex gap-3">
                    <button
                      onClick={closeModal}
                      className="px-6 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg transition-colors font-medium"
                    >
                      Close
                    </button>
                    <button
                      className="px-6 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors font-medium"
                      onClick={() => window.print()}
                    >
                      Print Report
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
}

export default UploadPage;
