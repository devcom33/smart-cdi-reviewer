          <div className="mx-auto max-w-4xl">
            <ul className="space-y-6">
              {clauses.map((clause) => (
                <li
                  key={clause.clause_index}
                  className="group relative overflow-hidden rounded-3xl bg-white/70 backdrop-blur-sm border border-white/20 shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
                >
                  {/* Gradient border effect */}
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-pink-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

                  <div className="relative p-6 space-y-4">
                    {/* Clause Index Badge */}
                    <div className="absolute top-4 right-4">
                      <span className="inline-flex items-center rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-800">
                        Clause {clause.clause_index}
                      </span>
                    </div>

                    {/* Main Clause Text */}
                    <div className="pr-20">
                      <h3 className="text-lg font-semibold text-gray-900 leading-relaxed">
                        {clause.clause_text}
                      </h3>
                    </div>

                    {/* Issue Section */}
                    {clause.issue && (
                      <div className="rounded-xl bg-red-50 border border-red-100 p-4">
                        <div className="flex items-start space-x-3">
                          <div className="flex-shrink-0">
                            <div className="h-6 w-6 rounded-full bg-red-100 flex items-center justify-center">
                              <svg
                                className="h-3 w-3 text-red-600"
                                fill="currentColor"
                                viewBox="0 0 20 20"
                              >
                                <path
                                  fillRule="evenodd"
                                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                                  clipRule="evenodd"
                                />
                              </svg>
                            </div>
                          </div>
                          <div>
                            <h4 className="text-sm font-medium text-red-800 mb-1">
                              Issue Identified
                            </h4>
                            <p className="text-sm text-red-700 leading-relaxed">
                              {clause.issue}
                            </p>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Suggestion Section */}
                    {clause.suggestion && (
                      <div className="rounded-xl bg-emerald-50 border border-emerald-100 p-4">
                        <div className="flex items-start space-x-3">
                          <div className="flex-shrink-0">
                            <div className="h-6 w-6 rounded-full bg-emerald-100 flex items-center justify-center">
                              <svg
                                className="h-3 w-3 text-emerald-600"
                                fill="currentColor"
                                viewBox="0 0 20 20"
                              >
                                <path
                                  fillRule="evenodd"
                                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                  clipRule="evenodd"
                                />
                              </svg>
                            </div>
                          </div>
                          <div>
                            <h4 className="text-sm font-medium text-emerald-800 mb-1">
                              Suggested Improvement
                            </h4>
                            <p className="text-sm text-emerald-700 leading-relaxed">
                              {clause.suggestion}
                            </p>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>