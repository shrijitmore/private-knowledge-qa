import { Link, useLocation } from "react-router-dom";
import { FileText, Upload, MessageSquare, Activity } from "lucide-react";

const navItems = [
  { path: "/", label: "Home", icon: FileText },
  { path: "/upload", label: "Upload", icon: Upload },
  { path: "/ask", label: "Ask", icon: MessageSquare },
  { path: "/status", label: "Status", icon: Activity },
];

export default function Layout({ children }) {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-background" data-testid="app-layout">
      <header className="sticky top-0 z-50 w-full border-b bg-background/80 backdrop-blur-xl supports-[backdrop-filter]:bg-background/60">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex h-14 items-center justify-between">
          <Link
            to="/"
            className="font-mono text-lg font-medium tracking-tight"
            data-testid="app-logo"
          >
            knowledge.qa
          </Link>
          <nav className="flex items-center gap-1" data-testid="main-nav">
            {navItems.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                data-testid={`nav-${label.toLowerCase()}`}
                className={`flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-150 ${
                  location.pathname === path
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                }`}
              >
                <Icon size={16} strokeWidth={1.5} />
                <span className="hidden sm:inline">{label}</span>
              </Link>
            ))}
          </nav>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {children}
      </main>
    </div>
  );
}
