import { useState, useEffect, useCallback } from "react";
import { Upload, FileText, Trash2, Loader2, AlertCircle } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export default function UploadPage() {
  const [docs, setDocs] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [loading, setLoading] = useState(true);

  const fetchDocs = async () => {
    try {
      const res = await fetch(`${API}/documents/`);
      const data = await res.json();
      setDocs(Array.isArray(data) ? data : []);
    } catch {
      setError("Failed to load documents");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocs();
  }, []);

  const handleUpload = async (files) => {
    setError(null);
    setSuccess(null);
    const file = files[0];
    if (!file) return;

    if (!file.name.endsWith('.txt')) {
      setError("Only .txt files are allowed");
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      setError("File too large (max 5MB)");
      return;
    }

    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const res = await fetch(`${API}/documents/upload`, {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Upload failed');
      }
      const result = await res.json();
      setSuccess(`Uploaded "${result.filename}" — ${result.chunk_count} chunks created`);
      await fetchDocs();
    } catch (e) {
      setError(e.message);
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (docId) => {
    try {
      const res = await fetch(`${API}/documents/${docId}`, { method: 'DELETE' });
      if (!res.ok) throw new Error("Delete failed");
      setDocs(prev => prev.filter(d => d.id !== docId));
    } catch (e) {
      setError(e.message);
    }
  };

  const onDragOver = useCallback((e) => {
    e.preventDefault();
    setDragOver(true);
  }, []);

  const onDragLeave = useCallback(() => setDragOver(false), []);

  const onDrop = useCallback((e) => {
    e.preventDefault();
    setDragOver(false);
    handleUpload(e.dataTransfer.files);
  }, []);

  return (
    <div className="space-y-10" data-testid="upload-page">
      <div>
        <h1 className="font-mono text-4xl md:text-5xl font-medium tracking-tight text-primary">
          Upload
        </h1>
        <p className="font-sans text-base text-muted-foreground mt-2">
          Add text documents to your knowledge base.
        </p>
      </div>

      {/* Drop Zone */}
      <div
        data-testid="upload-dropzone"
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        onClick={() => !uploading && document.getElementById('file-input').click()}
        className={`relative h-64 rounded-lg border-2 border-dashed transition-all duration-200 cursor-pointer flex flex-col items-center justify-center gap-4 ${
          dragOver
            ? "border-primary bg-primary/5"
            : "border-border hover:border-primary/50 hover:bg-muted/30"
        } ${uploading ? "pointer-events-none opacity-60" : ""}`}
      >
        <input
          id="file-input"
          type="file"
          accept=".txt"
          className="hidden"
          data-testid="file-input"
          onChange={(e) => {
            handleUpload(e.target.files);
            e.target.value = '';
          }}
        />
        {uploading ? (
          <>
            <Loader2 size={36} className="animate-spin text-muted-foreground" strokeWidth={1.5} />
            <p className="text-sm text-muted-foreground font-medium">Processing document...</p>
            <p className="text-xs text-muted-foreground">Chunking text & generating embeddings</p>
          </>
        ) : (
          <>
            <Upload size={36} className="text-muted-foreground" strokeWidth={1.5} />
            <div className="text-center">
              <p className="text-sm font-medium">Drop .txt file here or click to browse</p>
              <p className="text-xs text-muted-foreground mt-1">Maximum file size: 5MB</p>
            </div>
          </>
        )}
      </div>

      {/* Success */}
      {success && (
        <div
          className="flex items-center gap-2 p-3 rounded-md bg-green-500/10 text-green-700 border border-green-200"
          data-testid="upload-success"
        >
          <FileText size={16} strokeWidth={1.5} />
          <p className="text-sm">{success}</p>
        </div>
      )}

      {/* Error */}
      {error && (
        <div
          className="flex items-center gap-2 p-3 rounded-md bg-red-500/10 text-red-600 border border-red-200"
          data-testid="upload-error"
        >
          <AlertCircle size={16} strokeWidth={1.5} />
          <p className="text-sm">{error}</p>
        </div>
      )}

      {/* Document List */}
      <div>
        <h2 className="font-mono text-xs uppercase tracking-wider text-muted-foreground mb-4">
          Documents ({docs.length})
        </h2>
        {loading ? (
          <div className="space-y-3">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-16 bg-muted animate-pulse rounded-lg" />
            ))}
          </div>
        ) : docs.length === 0 ? (
          <Card>
            <CardContent className="py-16 text-center text-muted-foreground">
              <FileText size={36} className="mx-auto mb-4 opacity-30" strokeWidth={1} />
              <p className="text-sm">No documents uploaded yet</p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-2">
            {docs.map(doc => (
              <div
                key={doc.id}
                className="flex items-center gap-4 p-4 rounded-lg border hover:shadow-sm transition-shadow duration-200"
                data-testid={`doc-item-${doc.id}`}
              >
                <FileText size={20} className="text-muted-foreground shrink-0" strokeWidth={1.5} />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">{doc.filename}</p>
                  <div className="flex items-center gap-3 mt-1">
                    <span className="text-xs text-muted-foreground font-mono">
                      {(doc.file_size / 1024).toFixed(1)} KB
                    </span>
                    <span className="text-xs text-muted-foreground">
                      {doc.chunk_count} chunks
                    </span>
                    <span className="text-xs text-muted-foreground">
                      {new Date(doc.uploaded_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDelete(doc.id);
                  }}
                  data-testid={`delete-doc-${doc.id}`}
                  className="text-muted-foreground hover:text-red-600"
                >
                  <Trash2 size={16} strokeWidth={1.5} />
                </Button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
