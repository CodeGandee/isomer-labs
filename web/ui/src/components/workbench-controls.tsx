import type * as React from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

type Tone = "default" | "muted" | "success" | "warning" | "danger" | "info";

export function ToolbarButton({ className, variant = "outline", size = "sm", ...props }: React.ComponentProps<typeof Button>) {
  return <Button className={cn("workbench-toolbar-button", className)} size={size} variant={variant} {...props} />;
}

export function LinkButton({ className, variant = "link", size = "sm", ...props }: React.ComponentProps<typeof Button>) {
  return <Button className={cn("link-button", className)} size={size} variant={variant} {...props} />;
}

export function StatusBadge({ className, tone = "muted", ...props }: React.ComponentProps<typeof Badge> & { tone?: Tone }) {
  return <Badge className={cn("status-badge", `status-badge-${tone}`, className)} variant="outline" {...props} />;
}
