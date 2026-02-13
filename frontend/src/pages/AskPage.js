import { useState, useEffect } from "react";
import { Send, Loader2, FileText, Clock, AlertCircle } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export default function AskPage() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetch(`${API}/qa/history`)
      .then(r => r.json())
      .then(data => setHistory(Array.isArray(data) ? data : []))
      .catch(() => {});
  }, []);

  const handleAsk = async (e) => {
    e.preventDefault();
    if (!question.trim() || loading) return;

    setError(null);
    setLoading(true);
    setAnswer(null);

    try {
      const res = await fetch(`${API}/qa/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question.trim() }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Failed to get answer');
      }
      const data = await res.json();
      setAnswer(data);
      setQuestion("");

      const histRes = await fetch(`${API}/qa/history`);
      const histData = await histRes.json();
      setHistory(Array.isArray(histData) ? histData : []);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-10" data-testid="ask-page">
      <div>
        <h1 className="font-mono text-4xl md:text-5xl font-medium tracking-tight text-primary">
          Ask
        </h1>
        <p className="font-sans text-base text-muted-foreground mt-2">
          Ask questions about your uploaded documents.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-8 space-y-6">
          {/* Input */}
          <form onSubmit={handleAsk} data-testid="ask-form">
            <div className="flex gap-3">
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask a question about your documents..."
                data-testid="question-input"
                className="flex-1 h-14 rounded-lg border-2 border-input bg-background px-5 text-base ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 transition-shadow"
                disabled={loading}
              />
              <Button
                type="submit"
                disabled={!question.trim() || loading}
                data-testid="ask-submit-btn"
                className="h-14 px-6"
              >
                {loading ? (
                  <Loader2 size={18} className="animate-spin" />
                ) : (
                  <Send size={18} strokeWidth={1.5} />
                )}
              </Button>
            </div>
          </form>

          {/* Error */}
          {error && (
            <div
              className="flex items-center gap-2 p-3 rounded-md bg-red-500/10 text-red-600 border border-red-200"
              data-testid="ask-error"
            >
              <AlertCircle size={16} strokeWidth={1.5} />
              <p className="text-sm">{error}</p>
            </div>
          )}

          {/* Loading */}
          {loading && (
            <Card data-testid="answer-loading">
              <CardContent className="p-6">
                <div className="flex items-center gap-3">
                  <Loader2 size={18} className="animate-spin text-muted-foreground" />
                  <p className="text-sm text-muted-foreground">
                    Searching documents and generating answer...
                  </p>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Answer */}
          {answer && (
            <div className="space-y-6" data-testid="answer-section">
              <Card>
                <CardContent className="p-6">
                  <p className="font-mono text-xs uppercase tracking-wider text-muted-foreground mb-4">
                    Answer
                  </p>
                  <div
                    className="text-sm leading-relaxed whitespace-pre-wrap"
                    data-testid="answer-text"
                  >
                    {answer.answer}
                  </div>
                </CardContent>
              </Card>

              {/* Sources */}
              {answer.sources && answer.sources.length > 0 && (
                <div>
                  <p className="font-mono text-xs uppercase tracking-wider text-muted-foreground mb-3">
                    Sources ({answer.sources.length})
                  </p>
                  <div className="space-y-2">
                    {answer.sources.map((source, i) => (
                      <div
                        key={i}
                        className="p-4 rounded-lg border border-l-4 border-l-primary/30"
                        data-testid={`source-${i}`}
                      >
                        <div className="flex items-center gap-2 mb-2">
                          <FileText
                            size={14}
                            className="text-muted-foreground"
                            strokeWidth={1.5}
                          />
                          <span className="font-mono text-xs font-medium">
                            {source.document_name}
                          </span>
                          <span className="text-xs text-muted-foreground">
                            chunk {source.chunk_index}
                          </span>
                          <span className="ml-auto font-mono text-xs text-muted-foreground">
                            {(source.similarity_score * 100).toFixed(0)}% match
                          </span>
                        </div>
                        <p className="text-xs text-muted-foreground leading-relaxed font-mono">
                          {source.chunk_text}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* History Sidebar */}
        <div className="lg:col-span-4">
          <div className="sticky top-20">
            <p className="font-mono text-xs uppercase tracking-wider text-muted-foreground mb-4">
              Recent Questions
            </p>
            {history.length === 0 ? (
              <Card>
                <CardContent className="py-12 text-center text-muted-foreground">
                  <Clock size={24} className="mx-auto mb-2 opacity-30" strokeWidth={1} />
                  <p className="text-xs">No questions yet</p>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-2">
                {history.map(item => (
                  <Card
                    key={item.id}
                    className="cursor-pointer hover:-translate-y-0.5 transition-transform duration-200"
                    data-testid={`history-item-${item.id}`}
                    onClick={() => setQuestion(item.question)}
                  >
                    <CardContent className="p-3">
                      <p className="text-sm font-medium line-clamp-2">{item.question}</p>
                      <p className="text-xs text-muted-foreground mt-1 line-clamp-1">
                        {item.answer}
                      </p>
                      <p className="text-xs text-muted-foreground mt-1 font-mono">
                        {new Date(item.timestamp).toLocaleString()}
                      </p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
