import { useState, useEffect } from "react";
import { RefreshCw, Loader2, CheckCircle, XCircle, Database, Server, Cpu, HardDrive } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const statusConfig = {
  backend: { icon: Server, label: "Backend API" },
  database: { icon: Database, label: "MongoDB" },
  llm: { icon: Cpu, label: "Gemini LLM" },
  vectorstore: { icon: HardDrive, label: "FAISS Vector Store" },
};

export default function StatusPage() {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchStatus = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API}/status/health`);
      if (!res.ok) throw new Error("Health check failed");
      setStatus(await res.json());
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  const isHealthy = (s) => s === "healthy" || s === "connected";

  return (
    <div className="space-y-10" data-testid="status-page">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="font-mono text-4xl md:text-5xl font-medium tracking-tight text-primary">
            Status
          </h1>
          <p className="font-sans text-base text-muted-foreground mt-2">
            System health and connectivity checks.
          </p>
        </div>
        <Button
          variant="outline"
          onClick={fetchStatus}
          disabled={loading}
          data-testid="refresh-status-btn"
          className="shrink-0"
        >
          {loading ? (
            <Loader2 size={16} className="animate-spin" />
          ) : (
            <RefreshCw size={16} strokeWidth={1.5} />
          )}
          <span className="ml-2">Refresh</span>
        </Button>
      </div>

      {error && (
        <div
          className="p-4 rounded-md bg-red-500/10 text-red-600 border border-red-200"
          data-testid="status-error"
        >
          <p className="text-sm">{error}</p>
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {Object.entries(statusConfig).map(([key, { icon: Icon, label }]) => {
          const s = status?.[key];
          const healthy = s && isHealthy(s.status);

          return (
            <Card key={key} data-testid={`status-${key}`}>
              <CardContent className="p-6">
                <div className="flex items-start gap-4">
                  <div
                    className={`w-10 h-10 rounded-md flex items-center justify-center ${
                      loading
                        ? "bg-muted"
                        : healthy
                        ? "bg-green-500/10"
                        : "bg-red-500/10"
                    }`}
                  >
                    <Icon
                      size={18}
                      className={
                        loading
                          ? "text-muted-foreground"
                          : healthy
                          ? "text-green-600"
                          : "text-red-600"
                      }
                      strokeWidth={1.5}
                    />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <p className="font-mono text-sm font-medium">{label}</p>
                      {!loading &&
                        s &&
                        (healthy ? (
                          <CheckCircle size={14} className="text-green-600" />
                        ) : (
                          <XCircle size={14} className="text-red-600" />
                        ))}
                    </div>
                    {loading ? (
                      <div className="h-4 w-32 bg-muted animate-pulse rounded mt-1" />
                    ) : s ? (
                      <p className="text-xs text-muted-foreground mt-1">{s.message}</p>
                    ) : (
                      <p className="text-xs text-muted-foreground mt-1">Unavailable</p>
                    )}
                  </div>
                  {!loading && s && (
                    <div
                      className={`w-2 h-2 rounded-full mt-1.5 ${
                        healthy
                          ? "bg-green-500 shadow-[0_0_6px] shadow-green-500/50"
                          : "bg-red-500 shadow-[0_0_6px] shadow-red-500/50"
                      }`}
                    />
                  )}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
