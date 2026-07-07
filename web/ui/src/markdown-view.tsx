import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import rehypeKatex from "rehype-katex";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import mermaid from "mermaid";

export type MarkdownViewState = "loading" | "empty" | "ready";

export function MarkdownView({ content, state = "ready" }: { content: string; state?: MarkdownViewState }) {
  if (state !== "ready") {
    return (
      <div className={`markdown-view markdown-view-status markdown-view-${state}`}>
        <p>{content}</p>
      </div>
    );
  }
  return (
    <div className="markdown-view">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeKatex]}
        components={{
          code(props) {
            const className = props.className || "";
            const value = String(props.children || "");
            if (className.includes("language-mermaid")) {
              return <MermaidBlock chart={value} />;
            }
            return <code className={className}>{props.children}</code>;
          },
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}

function MermaidBlock({ chart }: { chart: string }) {
  const [svg, setSvg] = useState("");
  useEffect(() => {
    let cancelled = false;
    mermaid.initialize({ startOnLoad: false, securityLevel: "strict" });
    mermaid.render(`mmd-${crypto.randomUUID()}`, chart).then((result) => {
      if (!cancelled) {
        setSvg(result.svg);
      }
    });
    return () => {
      cancelled = true;
    };
  }, [chart]);
  return <div className="mermaid" dangerouslySetInnerHTML={{ __html: svg }} />;
}
