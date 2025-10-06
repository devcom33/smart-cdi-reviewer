import React, { useState } from "react";
import NavBar from "../components/NavBar";
import {
  Upload,
  Loader2,
  CheckCircle,
  AlertTriangle,
  FileText,
  Clock,
} from "lucide-react";
import { UploadService } from "../services/UploadService";
import { ResultService } from "../services/ResultService";

function UploadPage() {
  const [clauses, setClauses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [processingProgress, setProcessingProgress] = useState(0);
  const [analysisComplete, setAnalysisComplete] = useState(false);

  const subscribeToResult = (id, onResult) => {
    const eventSource = new EventSource(
      `http://localhost:8080/api/v1/result/subscribe/${id}`
    );

    eventSource.onmessage = (event) => {
      const result = JSON.parse(event.data);
      onResult(result);
      eventSource.close();
    };

    return eventSource;
  };

  const handleUpload = async (file) => {
    if (!file) return;

    setUploadedFile(file);
    setIsProcessing(true);
    setAnalysisComplete(false);
    setClauses([]);

    try {
      setLoading(true);

      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setProcessingProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + Math.random() * 15;
        });
      }, 500);

      const { id } = await UploadService(file);

      if (id) {
        subscribeToResult(id, (result) => {
          clearInterval(progressInterval);
          setProcessingProgress(100);
          setClauses(result.output);
          setAnalysisComplete(true);
          setIsProcessing(false);
          setLoading(false);
        });
      } else {
        console.error("Id not found");
        setIsProcessing(false);
        setLoading(false);
      }
    } catch (error) {
      setLoading(false);
      setIsProcessing(false);
      console.error("Error Uploading Contract:", error);
      throw error;
    }
  };

  const resetUpload = () => {
    setUploadedFile(null);
    setClauses([]);
    setIsProcessing(false);
    setAnalysisComplete(false);
    setProcessingProgress(0);
  };

  const getAnalysisSummary = () => {
    const totalClauses = clauses.length;
    const issuesCount = clauses.filter((clause) => clause.issue).length;
    const suggestionsCount = clauses.filter(
      (clause) => clause.suggestion
    ).length;

    return { totalClauses, issuesCount, suggestionsCount };
  };

  const { totalClauses, issuesCount, suggestionsCount } = getAnalysisSummary();

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

          {/* Upload Section */}
          <div className="bg-white rounded-xl shadow-lg p-8 mb-6">
            {!isProcessing && !analysisComplete ? (
              <div className="flex justify-center gap-4 flex-wrap">
                <div className="space-y-6 items-center text-center">
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
                </div>
              </div>
            ) : isProcessing ? (
              // Processing State
              <div className="text-center space-y-6">
                <div className="flex justify-center">
                  <div className="relative">
                    <Loader2 className="w-16 h-16 text-blue-500 animate-spin" />
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-xs font-semibold text-blue-600">
                        {Math.round(processingProgress)}%
                      </span>
                    </div>
                  </div>
                </div>

                <div className="space-y-3">
                  <h3 className="text-xl font-semibold text-gray-900">
                    Analyzing Contract
                  </h3>
                  <p className="text-gray-600">
                    Processing{" "}
                    <span className="font-medium">{uploadedFile?.name}</span>
                  </p>

                  {/* Progress Bar */}
                  <div className="w-full bg-gray-200 rounded-full h-2 max-w-md mx-auto">
                    <div
                      className="bg-blue-500 h-2 rounded-full transition-all duration-500 ease-out"
                      style={{ width: `${processingProgress}%` }}
                    ></div>
                  </div>

                  <p className="text-sm text-gray-500">
                    This may take a few minutes...
                  </p>
                </div>
              </div>
            ) : (
              // Analysis Complete State
              <div className="text-center space-y-6">
                <div className="flex justify-center">
                  <CheckCircle className="w-16 h-16 text-green-500" />
                </div>

                <div className="space-y-3">
                  <h3 className="text-xl font-semibold text-gray-900">
                    Analysis Complete!
                  </h3>
                  <p className="text-gray-600">
                    Your contract{" "}
                    <span className="font-medium">{uploadedFile?.name}</span>{" "}
                    has been analyzed
                  </p>

                  {/* Summary Stats */}
                  <div className="flex justify-center gap-6 pt-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-blue-600">
                        {totalClauses}
                      </div>
                      <div className="text-sm text-gray-500">Clauses</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-red-500">
                        {issuesCount}
                      </div>
                      <div className="text-sm text-gray-500">Issues</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-500">
                        {suggestionsCount}
                      </div>
                      <div className="text-sm text-gray-500">Suggestions</div>
                    </div>
                  </div>
                </div>

                <button
                  onClick={resetUpload}
                  className="inline-flex items-center gap-2 px-6 py-2 text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors"
                >
                  Upload Another Contract
                </button>
              </div>
            )}
          </div>

          {/* Results Section */}
          {analysisComplete && clauses.length > 0 && (
            <div className="space-y-6">
              {/* Results Header */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center gap-3 mb-4">
                  <FileText className="w-6 h-6 text-blue-500" />
                  <h3 className="text-xl font-semibold text-gray-900">
                    Contract Analysis Results
                  </h3>
                </div>

                {issuesCount > 0 ? (
                  <div className="flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                    <AlertTriangle className="w-5 h-5 text-amber-600 mt-0.5" />
                    <div>
                      <h4 className="font-medium text-amber-800">
                        {issuesCount} issue{issuesCount !== 1 ? "s" : ""} found
                      </h4>
                      <p className="text-sm text-amber-700">
                        Review the highlighted clauses below for potential
                        compliance concerns.
                      </p>
                    </div>
                  </div>
                ) : (
                  <div className="flex items-start gap-3 p-4 bg-green-50 border border-green-200 rounded-lg">
                    <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
                    <div>
                      <h4 className="font-medium text-green-800">
                        Contract looks good!
                      </h4>
                      <p className="text-sm text-green-700">
                        No major compliance issues were identified.
                      </p>
                    </div>
                  </div>
                )}
              </div>

              {/* Clauses List */}
              <div className="space-y-4">
                {clauses.map((clause, index) => (
                  <div
                    key={clause.clause_index}
                    className="group relative overflow-hidden rounded-xl bg-white shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
                  >
                    <div className="p-6 space-y-4">
                      {/* Clause Header */}
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <span className="inline-flex items-center rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-800">
                              Clause {clause.clause_index}
                            </span>
                            {clause.issue && (
                              <span className="inline-flex items-center rounded-full bg-red-100 px-3 py-1 text-xs font-medium text-red-800">
                                Issue Found
                              </span>
                            )}
                          </div>
                          <h4 className="text-lg font-medium text-gray-900 leading-relaxed">
                            {clause.clause_text}
                          </h4>
                        </div>
                      </div>

                      {/* Issue Section */}
                      {clause.issue && (
                        <div className="rounded-lg bg-red-50 border border-red-200 p-4">
                          <div className="flex items-start space-x-3">
                            <div className="flex-shrink-0">
                              <AlertTriangle className="h-5 w-5 text-red-500" />
                            </div>
                            <div>
                              <h5 className="text-sm font-semibold text-red-800 mb-1">
                                Compliance Issue
                              </h5>
                              <p className="text-sm text-red-700 leading-relaxed">
                                {clause.issue}
                              </p>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* Suggestion Section */}
                      {clause.suggestion && (
                        <div className="rounded-lg bg-green-50 border border-green-200 p-4">
                          <div className="flex items-start space-x-3">
                            <div className="flex-shrink-0">
                              <CheckCircle className="h-5 w-5 text-green-500" />
                            </div>
                            <div>
                              <h5 className="text-sm font-semibold text-green-800 mb-1">
                                Recommended Action
                              </h5>
                              <p className="text-sm text-green-700 leading-relaxed">
                                {clause.suggestion}
                              </p>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export default UploadPage;
