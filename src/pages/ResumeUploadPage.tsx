import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { Upload, FileText, X, CheckCircle } from "lucide-react";
import { resumeService } from "../services/resumeService";

const ResumeUploadPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [done, setDone] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    const f = e.dataTransfer.files[0];
    if (f && (f.type === "application/pdf" || f.name.endsWith(".docx"))) {
      setFile(f);
      setError("");
    }
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) {
      setFile(f);
      setError("");
    }
  };

  const handleAnalyze = async () => {
    if (!file) return;
    
    setAnalyzing(true);
    setError("");
    
    try {
      await resumeService.uploadResume(file);
      setDone(true);
      // Navigate to analysis page after successful upload
      setTimeout(() => {
        navigate("/resume-analysis");
      }, 1500);
    } catch (err: any) {
      // Handle different error formats
      let errorMessage = "Failed to upload resume. Please try again.";
      
      if (typeof err === 'string') {
        errorMessage = err;
      } else if (err?.detail) {
        if (typeof err.detail === 'string') {
          errorMessage = err.detail;
        } else if (err.detail?.msg) {
          errorMessage = err.detail.msg;
        } else if (err.detail?.message) {
          errorMessage = err.detail.message;
        }
      } else if (err?.message) {
        errorMessage = err.message;
      } else if (err?.error) {
        errorMessage = err.error;
      }
      
      setError(errorMessage);
      setDone(false);
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Upload Resume</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Upload your resume for AI-powered analysis and feedback.
        </p>
      </div>

      {/* Error message */}
      {error && (
        <div className="p-3 rounded-lg bg-destructive/10 text-destructive text-sm">
          {error}
        </div>
      )}

      {/* Drop zone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
        className={`flex flex-col items-center justify-center rounded-xl border-2 border-dashed p-12 transition-colors ${
          dragActive
            ? "border-primary bg-primary/5"
            : "border-border hover:border-primary/40"
        }`}
      >
        <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-primary/10 mb-4">
          <Upload className="h-7 w-7 text-primary" />
        </div>
        <p className="text-sm font-medium text-foreground">
          Drag & drop your resume here
        </p>
        <p className="mt-1 text-xs text-muted-foreground">
          PDF or DOCX, up to 10MB
        </p>
        <label className="mt-4 cursor-pointer rounded-lg border border-border bg-card px-4 py-2 text-sm font-medium text-foreground hover:bg-accent transition-colors">
          Browse Files
          <input
            type="file"
            accept=".pdf,.docx"
            onChange={handleFileChange}
            className="hidden"
          />
        </label>
      </div>

      {/* File preview */}
      {file && (
        <div className="flex items-center justify-between rounded-xl border border-border bg-card p-4 card-shadow">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
              <FileText className="h-5 w-5 text-primary" />
            </div>
            <div>
              <p className="text-sm font-medium text-foreground">{file.name}</p>
              <p className="text-xs text-muted-foreground">
                {(file.size / 1024).toFixed(1)} KB
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {done && <CheckCircle className="h-5 w-5 text-success" />}
            <button
              onClick={() => { setFile(null); setDone(false); setError(""); }}
              className="text-muted-foreground hover:text-destructive transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>
      )}

      {file && !done && (
        <button
          onClick={handleAnalyze}
          disabled={analyzing}
          className="w-full rounded-lg gradient-primary px-4 py-3 text-sm font-semibold text-primary-foreground hover:opacity-90 transition-opacity disabled:opacity-60"
        >
          {analyzing ? "Analyzing..." : "Analyze Resume"}
        </button>
      )}

      {done && (
        <div className="rounded-xl border border-success/20 bg-success/5 p-4 text-center">
          <CheckCircle className="mx-auto h-8 w-8 text-success mb-2" />
          <p className="text-sm font-medium text-foreground">Analysis Complete!</p>
          <p className="text-xs text-muted-foreground mt-1">
            View your results on the Resume Analysis page.
          </p>
        </div>
      )}
    </div>
  );
};

export default ResumeUploadPage;
