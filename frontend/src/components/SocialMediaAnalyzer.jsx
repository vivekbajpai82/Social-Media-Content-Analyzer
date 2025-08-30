import React, { useState, useEffect, useRef } from 'react';

const SocialMediaAnalyzer = () => {
  const [fileInfo, setFileInfo] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef(null);
  //const apiUrl = 'http://localhost:5000/api';
  const apiUrl = import.meta.env.VITE_API_URL;


  // File validation
  const isValidFile = (file) => {
    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
    return allowedTypes.includes(file.type);
  };

  // Format file size
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  // Capitalize first letter
  const capitalizeFirst = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
  };

  // Get readability description
  const getReadabilityDescription = (score) => {
    if (!score) return 'Unknown';
    if (score >= 90) return 'Very Easy';
    if (score >= 80) return 'Easy';
    if (score >= 70) return 'Fairly Easy';
    if (score >= 60) return 'Standard';
    if (score >= 50) return 'Fairly Difficult';
    if (score >= 30) return 'Difficult';
    return 'Very Difficult';
  };

  // Handle file selection/drop
  const handleFiles = async (files) => {
    if (files.length === 0) return;

    const file = files[0];
    
    if (!isValidFile(file)) {
      setError('Please upload a PDF or image file (JPG, PNG, JPEG)');
      setTimeout(() => setError(''), 5000);
      return;
    }

    setFileInfo({
      name: file.name,
      size: formatFileSize(file.size)
    });
    setIsProcessing(true);
    setError('');
    setResults(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${apiUrl}/upload`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Upload failed');
      }

      const data = await response.json();
      console.log('Backend Response:', data);
      setResults(data);
      setIsProcessing(false);

    } catch (error) {
      console.error('Error:', error);
      setError(error.message);
      setIsProcessing(false);
    }
  };

  // Drag and drop handlers
  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
  };

  const handleFileInputChange = (e) => {
    const files = Array.from(e.target.files);
    handleFiles(files);
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  const handleReset = () => {
    setFileInfo(null);
    setIsProcessing(false);
    setResults(null);
    setError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handlePrint = () => {
    window.print();
  };

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.ctrlKey && e.key === 'u') {
        e.preventDefault();
        fileInputRef.current?.click();
      }
      if (e.key === 'Escape') {
        handleReset();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div style={{
      fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
      minHeight: '100vh',
      padding: '20px',
      position: 'relative',
      background: 'linear-gradient(rgba(102, 126, 234, 0.6), rgba(132, 104, 159, 0.6))',
      backgroundSize: 'cover',
      backgroundPosition: 'center'
    }}>
      
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        background: 'rgb(89, 79, 99)',
        borderRadius: '20px',
        boxShadow: '0 20px 40px rgba(0,0,0,0.1)',
        overflow: 'auto'
      }}>
        
        {/* Header */}
        <header style={{
          background: 'linear-gradient(45deg, #11051e, #764ba2)',
          color: 'white',
          padding: '30px',
          textAlign: 'center'
        }}>
          <h1 style={{
            fontSize: '2.5em',
            marginBottom: '10px',
            fontWeight: '700',
            margin: '0 0 10px 0'
          }}>
            📱 Social Media Content Analyzer
          </h1>
          <p style={{
            fontSize: '1.1em',
            opacity: '0.9',
            margin: 0
          }}>
            Upload your content and get AI-powered engagement suggestions
          </p>
        </header>

        {/* Main Content */}
        <main style={{ padding: '40px' }}>
          
          {/* Upload Section */}
          <section>
            <div
              style={{
                border: `3px dashed ${isDragOver ? '#4CAF50' : '#667eea'}`,
                borderRadius: '15px',
                padding: '60px 30px',
                textAlign: 'center',
                marginBottom: '30px',
                background: isDragOver ? '#e8f5e8' : '#f8f9ff',
                transition: 'all 0.3s ease',
                cursor: 'pointer'
              }}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={handleBrowseClick}
            >
              <div style={{
                fontSize: '4em',
                color: '#667eea',
                marginBottom: '20px'
              }}>📁</div>
              <h3 style={{ margin: '0 0 15px 0', fontSize: '1.3em', color: '#333' }}>
                Upload Your Content
              </h3>
              <p style={{ color: '#666', fontSize: '1em', margin: '0 0 20px 0' }}>
                Drag & drop PDF or image files here, or click to browse
              </p>
              <input
                type="file"
                ref={fileInputRef}
                accept=".pdf,.jpg,.jpeg,.png"
                style={{ display: 'none' }}
                onChange={handleFileInputChange}
              />
              <button
                style={{
                  background: 'linear-gradient(45deg, #667eea, #764ba2)',
                  color: 'white',
                  border: 'none',
                  padding: '12px 30px',
                  borderRadius: '25px',
                  fontSize: '1em',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  margin: '10px'
                }}
                onClick={(e) => {
                  e.stopPropagation();
                  handleBrowseClick();
                }}
                onMouseOver={(e) => {
                  e.target.style.transform = 'translateY(-2px)';
                  e.target.style.boxShadow = '0 5px 15px rgba(102, 126, 234, 0.4)';
                }}
                onMouseOut={(e) => {
                  e.target.style.transform = 'translateY(0)';
                  e.target.style.boxShadow = 'none';
                }}
              >
                Choose File
              </button>
              <div style={{ marginTop: '15px' }}>
                <small style={{ color: '#666' }}>
                  Supported formats: PDF, JPG, PNG, JPEG
                </small>
              </div>
            </div>

            {/* File Info */}
            {fileInfo && (
              <div style={{
                display: 'flex',
                alignItems: 'center',
                background: '#e8f5e8',
                padding: '15px',
                borderRadius: '10px',
                margin: '20px 0',
                borderLeft: '4px solid #4CAF50'
              }}>
                <div style={{ fontSize: '2em', marginRight: '15px' }}>📄</div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>
                    {fileInfo.name} ({fileInfo.size})
                  </div>
                  <div style={{ color: '#666', fontSize: '0.9em' }}>
                    Ready to analyze
                  </div>
                </div>
                <button
                  style={{
                    background: 'transparent',
                    border: 'none',
                    fontSize: '1.5em',
                    cursor: 'pointer',
                    color: '#666'
                  }}
                  onClick={handleReset}
                >
                  ×
                </button>
              </div>
            )}
          </section>

          {/* Processing Section */}
          {isProcessing && (
            <section style={{
              textAlign: 'center',
              padding: '30px'
            }}>
              <div style={{ color: '#e0e0e0', fontWeight: 'bold', textShadow: '1px 1px 3px rgba(0,0,0,0.5)' }}>
                <div style={{
                  border: '4px solid #f3f3f3',
                  borderTop: '4px solid #667eea',
                  borderRadius: '50%',
                  width: '50px',
                  height: '50px',
                  animation: 'spin 1s linear infinite',
                  margin: '0 auto 20px'
                }}></div>
                <h3 style={{ margin: '0 0 10px 0' }}>Processing your content...</h3>
                <p style={{ margin: '0 0 20px 0' }}>Extracting text and analyzing for social media optimization</p>
                <div>
                  <div style={{ margin: '10px 0' }}>📄 Extracting text</div>
                  <div style={{ margin: '10px 0' }}>🤖 AI analysis</div>
                  <div style={{ margin: '10px 0' }}>📊 Generating insights</div>
                </div>
              </div>
            </section>
          )}

          {/* Error Section */}
          {error && (
            <div style={{
              background: '#ffebee',
              color: '#c62828',
              padding: '15px',
              borderRadius: '10px',
              margin: '20px 0',
              borderLeft: '4px solid #c62828'
            }}>
              {error}
            </div>
          )}

          {/* Results Section */}
          {results && !isProcessing && (
            <section>
              {/* Content Analytics */}
              <div style={{
                background: '#f8f9ff',
                borderRadius: '15px',
                padding: '25px',
                marginBottom: '20px',
                borderLeft: '5px solid #667eea'
              }}>
                <div style={{
                  fontSize: '1.3em',
                  color: '#333',
                  marginBottom: '15px',
                  fontWeight: '600'
                }}>
                  📊 Content Analytics
                </div>
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                  gap: '20px',
                  marginTop: '20px'
                }}>
                  {results.analysis?.metrics && Object.entries({
                    'Words': results.analysis.metrics.word_count || 0,
                    'Characters': results.analysis.metrics.character_count || 0,
                    'Sentences': results.analysis.metrics.sentence_count || 0,
                    'Avg Words/Sentence': results.analysis.metrics.avg_words_per_sentence || 0,
                    'Avg Chars/Word': results.analysis.metrics.avg_chars_per_word || 0
                  }).map(([label, value]) => (
                    <div key={label} style={{
                      background: 'white',
                      padding: '20px',
                      borderRadius: '10px',
                      textAlign: 'center',
                      boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
                    }}>
                      <div style={{
                        fontSize: '2em',
                        fontWeight: 'bold',
                        color: '#667eea'
                      }}>
                        {value}
                      </div>
                      <div style={{
                        color: '#666',
                        marginTop: '5px'
                      }}>
                        {label}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Extracted Text */}
              <div style={{
                background: '#f8f9ff',
                borderRadius: '15px',
                padding: '25px',
                marginBottom: '20px',
                borderLeft: '5px solid #667eea'
              }}>
                <div style={{
                  fontSize: '1.3em',
                  color: '#333',
                  marginBottom: '15px',
                  fontWeight: '600'
                }}>
                  📝 Extracted Text
                </div>
                <div style={{
                  background: 'white',
                  border: '1px solid #ddd',
                  borderRadius: '10px',
                  padding: '20px',
                  maxHeight: '300px',
                  overflowY: 'auto',
                  fontFamily: "'Courier New', monospace",
                  lineHeight: '1.6',
                  whiteSpace: 'pre-wrap',
                  wordWrap: 'break-word'
                }}>
                  {results.extracted_text || 'No text extracted'}
                </div>
              </div>

              {/* Platform Analysis */}
              <div style={{
                background: '#f8f9ff',
                borderRadius: '15px',
                padding: '25px',
                marginBottom: '20px',
                borderLeft: '5px solid #667eea'
              }}>
                <div style={{
                  fontSize: '1.3em',
                  color: '#333',
                  marginBottom: '15px',
                  fontWeight: '600'
                }}>
                  🎯 Platform Analysis
                </div>
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                  gap: '15px',
                  marginTop: '20px'
                }}>
                  {results.analysis?.platform_analysis && Object.entries(results.analysis.platform_analysis).map(([platform, data]) => (
                    <div key={platform} style={{
                      background: 'white',
                      padding: '20px',
                      borderRadius: '10px',
                      boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
                    }}>
                      <div style={{
                        fontWeight: '600',
                        fontSize: '1.1em',
                        marginBottom: '10px',
                        textTransform: 'capitalize'
                      }}>
                        {capitalizeFirst(platform)}
                      </div>
                      <div style={{
                        margin: '5px 0',
                        fontSize: '0.9em',
                        color: data.suitable ? '#4CAF50' : '#f44336'
                      }}>
                        {data.recommendation || 'No recommendation available'}
                      </div>
                      <div style={{ fontSize: '0.8em', color: '#666', marginTop: '10px' }}>
                        <span>Usage: {data.char_usage || 'N/A'}</span>
                        <span> ({data.char_percentage || 0}%)</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Improvement Suggestions */}
              <div style={{
                background: '#f8f9ff',
                borderRadius: '15px',
                padding: '25px',
                marginBottom: '20px',
                borderLeft: '5px solid #667eea'
              }}>
                <div style={{
                  fontSize: '1.3em',
                  color: '#333',
                  marginBottom: '15px',
                  fontWeight: '600'
                }}>
                  🚀 Improvement Suggestions
                </div>
                <div style={{
                  background: 'white',
                  border: '1px solid #ddd',
                  borderRadius: '10px',
                  padding: '20px'
                }}>
                  {results.analysis?.suggestions && results.analysis.suggestions.length > 0 ? (
                    results.analysis.suggestions.map((suggestion, index) => (
                      <div key={index} style={{
                        padding: '15px',
                        margin: '10px 0',
                        background: '#f0f8ff',
                        borderRadius: '8px',
                        borderLeft: `4px solid ${
                          suggestion.priority === 'high' ? '#ff4444' : 
                          suggestion.priority === 'medium' ? '#ffaa00' : '#44ff44'
                        }`
                      }}>
                        <div style={{
                          fontWeight: '600',
                          color: '#667eea',
                          marginBottom: '5px'
                        }}>
                          {suggestion.type || 'General'}
                        </div>
                        <div>{suggestion.suggestion || suggestion}</div>
                        {suggestion.action && (
                          <div style={{ marginTop: '5px', fontSize: '0.9em' }}>
                            <strong>Action:</strong> {suggestion.action}
                          </div>
                        )}
                      </div>
                    ))
                  ) : (
                    <p>No suggestions available</p>
                  )}
                </div>
              </div>

              {/* Social Media Elements */}
              <div style={{
                background: '#f8f9ff',
                borderRadius: '15px',
                padding: '25px',
                marginBottom: '20px',
                borderLeft: '5px solid #667eea'
              }}>
                <div style={{
                  fontSize: '1.3em',
                  color: '#333',
                  marginBottom: '15px',
                  fontWeight: '600'
                }}>
                  📈 Social Media Elements
                </div>
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                  gap: '15px'
                }}>
                  {results.analysis?.social_analysis ? (
                    <>
                      {results.analysis.social_analysis.hashtags && (
                        <div style={{
                          background: 'white',
                          padding: '15px',
                          borderRadius: '10px',
                          textAlign: 'center'
                        }}>
                          <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>Hashtags</div>
                          <div style={{ fontSize: '1.5em', color: '#667eea' }}>
                            {results.analysis.social_analysis.hashtags.count || 0}
                          </div>
                          {results.analysis.social_analysis.hashtags.list?.length > 0 && (
                            <div style={{ fontSize: '0.8em', color: '#666', marginTop: '5px' }}>
                              {results.analysis.social_analysis.hashtags.list.join(', ')}
                            </div>
                          )}
                        </div>
                      )}
                      {results.analysis.social_analysis.mentions && (
                        <div style={{
                          background: 'white',
                          padding: '15px',
                          borderRadius: '10px',
                          textAlign: 'center'
                        }}>
                          <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>Mentions</div>
                          <div style={{ fontSize: '1.5em', color: '#667eea' }}>
                            {results.analysis.social_analysis.mentions.count || 0}
                          </div>
                        </div>
                      )}
                      {results.analysis.social_analysis.urls && (
                        <div style={{
                          background: 'white',
                          padding: '15px',
                          borderRadius: '10px',
                          textAlign: 'center'
                        }}>
                          <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>URLs</div>
                          <div style={{ fontSize: '1.5em', color: '#667eea' }}>
                            {results.analysis.social_analysis.urls.count || 0}
                          </div>
                        </div>
                      )}
                      {results.analysis.social_analysis.emojis && (
                        <div style={{
                          background: 'white',
                          padding: '15px',
                          borderRadius: '10px',
                          textAlign: 'center'
                        }}>
                          <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>Emojis</div>
                          <div style={{ fontSize: '1.5em', color: '#667eea' }}>
                            {results.analysis.social_analysis.emojis.count || 0}
                          </div>
                        </div>
                      )}
                      <div style={{
                        background: 'white',
                        padding: '15px',
                        borderRadius: '10px',
                        textAlign: 'center'
                      }}>
                        <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>Questions</div>
                        <div style={{ fontSize: '1.5em', color: '#667eea' }}>
                          {results.analysis.social_analysis.questions || 0}
                        </div>
                      </div>
                      <div style={{
                        background: 'white',
                        padding: '15px',
                        borderRadius: '10px',
                        textAlign: 'center'
                      }}>
                        <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>Exclamations</div>
                        <div style={{ fontSize: '1.5em', color: '#667eea' }}>
                          {results.analysis.social_analysis.exclamations || 0}
                        </div>
                      </div>
                      <div style={{
                        background: 'white',
                        padding: '15px',
                        borderRadius: '10px',
                        textAlign: 'center'
                      }}>
                        <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>CTA Elements</div>
                        <div style={{ fontSize: '1.5em', color: '#667eea' }}>
                          {results.analysis.social_analysis.cta_elements || 0}
                        </div>
                      </div>
                    </>
                  ) : (
                    <p>No social media elements found</p>
                  )}
                </div>
              </div>

              {/* Readability Analysis */}
              <div style={{
                background: '#f8f9ff',
                borderRadius: '15px',
                padding: '25px',
                marginBottom: '20px',
                borderLeft: '5px solid #667eea'
              }}>
                <div style={{
                  fontSize: '1.3em',
                  color: '#333',
                  marginBottom: '15px',
                  fontWeight: '600'
                }}>
                  📖 Readability Analysis
                </div>
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                  gap: '15px'
                }}>
                  {results.analysis?.readability ? (
                    <>
                      <div style={{
                        background: 'white',
                        padding: '20px',
                        borderRadius: '10px',
                        textAlign: 'center'
                      }}>
                        <div style={{ fontWeight: 'bold', marginBottom: '10px' }}>Flesch Reading Ease</div>
                        <div style={{ fontSize: '2em', color: '#667eea', marginBottom: '5px' }}>
                          {Math.round(results.analysis.readability.flesch_reading_ease || 0)}
                        </div>
                        <div style={{ fontSize: '0.9em', color: '#666' }}>
                          {getReadabilityDescription(results.analysis.readability.flesch_reading_ease)}
                        </div>
                      </div>
                      <div style={{
                        background: 'white',
                        padding: '20px',
                        borderRadius: '10px',
                        textAlign: 'center'
                      }}>
                        <div style={{ fontWeight: 'bold', marginBottom: '10px' }}>Grade Level</div>
                        <div style={{ fontSize: '2em', color: '#667eea', marginBottom: '5px' }}>
                          {Math.round(results.analysis.readability.flesch_kincaid_grade || 0)}
                        </div>
                        <div style={{ fontSize: '0.9em', color: '#666' }}>
                          Grade {Math.round(results.analysis.readability.flesch_kincaid_grade || 0)} level
                        </div>
                      </div>
                      <div style={{
                        background: 'white',
                        padding: '20px',
                        borderRadius: '10px',
                        textAlign: 'center'
                      }}>
                        <div style={{ fontWeight: 'bold', marginBottom: '10px' }}>Reading Time</div>
                        <div style={{ fontSize: '2em', color: '#667eea', marginBottom: '5px' }}>
                          {results.analysis.readability.reading_time_minutes || 0} min
                        </div>
                        <div style={{ fontSize: '0.9em', color: '#666' }}>
                          Average reading time
                        </div>
                      </div>
                    </>
                  ) : (
                    <p>No readability data available</p>
                  )}
                </div>
              </div>

              {/* Action Buttons */}
              <div style={{ textAlign: 'center', marginTop: '30px' }}>
                <button
                  style={{
                    background: 'linear-gradient(45deg, #667eea, #764ba2)',
                    color: 'white',
                    border: 'none',
                    padding: '12px 30px',
                    borderRadius: '25px',
                    fontSize: '1em',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease',
                    margin: '10px'
                  }}
                  onClick={handleReset}
                  onMouseOver={(e) => {
                    e.target.style.transform = 'translateY(-2px)';
                    e.target.style.boxShadow = '0 5px 15px rgba(102, 126, 234, 0.4)';
                  }}
                  onMouseOut={(e) => {
                    e.target.style.transform = 'translateY(0)';
                    e.target.style.boxShadow = 'none';
                  }}
                >
                  🔄 Analyze Another File
                </button>
                <button
                  style={{
                    background: '#6c757d',
                    color: 'white',
                    border: 'none',
                    padding: '12px 30px',
                    borderRadius: '25px',
                    fontSize: '1em',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease',
                    margin: '10px'
                  }}
                  onClick={handlePrint}
                  onMouseOver={(e) => {
                    e.target.style.transform = 'translateY(-2px)';
                    e.target.style.boxShadow = '0 5px 15px rgba(108, 117, 125, 0.4)';
                  }}
                  onMouseOut={(e) => {
                    e.target.style.transform = 'translateY(0)';
                    e.target.style.boxShadow = 'none';
                  }}
                >
                  🖨️ Print Results
                </button>
              </div>
            </section>
          )}
        </main>
      </div>

      {/* Add CSS for spinner animation */}
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        body.dragging {
          background-color: rgba(102, 126, 234, 0.1);
        }
      `}</style>
    </div>
  );
};

export default SocialMediaAnalyzer;