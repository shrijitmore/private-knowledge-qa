import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Upload, MessageSquare, FileText, ArrowRight, Clock } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export default function HomePage() {
  const [docs, setDocs] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/documents/`).then(r => r.json()).catch(() => []),
      fetch(`${API}/qa/history`).then(r => r.json()).catch(() => []),
    ]).then(([d, h]) => {
      setDocs(Array.isArray(d) ? d : []);
      setHistory(Array.isArray(h) ? h : []);
      setLoading(false);
    });
  }, []);

  return (
    <div className="space-y-10" data-testid="home-page">
      <div>
        <h1 className="font-mono text-4xl md:text-5xl font-medium tracking-tight text-primary">
          Knowledge Q&A
        </h1>
        <p className="font-sans text-lg leading-relaxed font-light text-muted-foreground mt-3">
          Upload documents. Ask questions. Get grounded answers.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        {/* Quick Actions */}
        <div className="md:col-span-4 space-y-4">
          <Card className="hover:-translate-y-0.5 transition-transform duration-200">
            <CardContent className="p-6">
              <Link to="/upload" data-testid="quick-upload-link" className="block">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-md bg-primary flex items-center justify-center">
                    <Upload size={20} className="text-primary-foreground" strokeWidth={1.5} />
                  </div>
                  <div className="flex-1">
                    <p className="font-mono text-sm font-medium">Upload</p>
                    <p className="text-xs text-muted-foreground">{docs.length} document{docs.length !== 1 ? 's' : ''}</p>
                  </div>
                  <ArrowRight size={16} className="text-muted-foreground" />
                </div>
              </Link>
            </CardContent>
          </Card>

          <Card className="hover:-translate-y-0.5 transition-transform duration-200">
            <CardContent className="p-6">
              <Link to="/ask" data-testid="quick-ask-link" className="block">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-md bg-secondary flex items-center justify-center">
                    <MessageSquare size={20} className="text-secondary-foreground" strokeWidth={1.5} />
                  </div>
                  <div className="flex-1">
                    <p className="font-mono text-sm font-medium">Ask</p>
                    <p className="text-xs text-muted-foreground">{history.length} recent quer{history.length !== 1 ? 'ies' : 'y'}</p>
                  </div>
                  <ArrowRight size={16} className="text-muted-foreground" />
                </div>
              </Link>
            </CardContent>
          </Card>
        </div>

        {/* Documents */}
        <div className="md:col-span-8">
          <Card>
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="font-mono text-xs uppercase tracking-wider text-muted-foreground">
                  Documents
                </CardTitle>
                <Link to="/upload">
                  <Button variant="ghost" size="sm" data-testid="view-all-docs-btn">
                    View All
                  </Button>
                </Link>
              </div>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="space-y-3">
                  {[1, 2, 3].map(i => (
                    <div key={i} className="h-12 bg-muted animate-pulse rounded" />
                  ))}
                </div>
              ) : docs.length === 0 ? (
                <div className="text-center py-16 text-muted-foreground">
                  <FileText size={36} className="mx-auto mb-4 opacity-30" strokeWidth={1} />
                  <p className="font-sans text-sm">No documents yet</p>
                  <Link to="/upload">
                    <Button variant="outline" size="sm" className="mt-4" data-testid="upload-first-doc-btn">
                      Upload your first document
                    </Button>
                  </Link>
                </div>
              ) : (
                <div className="space-y-2">
                  {docs.slice(0, 5).map(doc => (
                    <div
                      key={doc.id}
                      className="flex items-center gap-3 p-3 rounded-md border"
                      data-testid={`home-doc-${doc.id}`}
                    >
                      <FileText size={16} className="text-muted-foreground shrink-0" strokeWidth={1.5} />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium truncate">{doc.filename}</p>
                        <p className="text-xs text-muted-foreground">{doc.chunk_count} chunks</p>
                      </div>
                      <span className="text-xs text-muted-foreground font-mono">
                        {(doc.file_size / 1024).toFixed(1)}KB
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Recent Q&A */}
      {history.length > 0 && (
        <div>
          <h2 className="font-mono text-xs uppercase tracking-wider text-muted-foreground mb-4">
            Recent Questions
          </h2>
          <div className="space-y-3">
            {history.slice(0, 3).map(item => (
              <Card
                key={item.id}
                className="hover:-translate-y-0.5 transition-transform duration-200"
                data-testid={`home-history-${item.id}`}
              >
                <CardContent className="p-4">
                  <div className="flex items-start gap-3">
                    <Clock size={14} className="text-muted-foreground mt-1 shrink-0" strokeWidth={1.5} />
                    <div className="min-w-0">
                      <p className="text-sm font-medium">{item.question}</p>
                      <p className="text-xs text-muted-foreground mt-1 line-clamp-2">{item.answer}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
