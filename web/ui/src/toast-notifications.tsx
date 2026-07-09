import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { createPortal } from "react-dom";

import {
  Toast,
  ToastClose,
  ToastDescription,
  ToastProvider,
  ToastTitle,
  ToastViewport,
} from "@/components/ui/toast";

const MAX_VISIBLE_TOASTS = 5;

export type ToastTone = "default" | "success" | "error" | "warning" | "info";

export type ToastNotification = {
  title: string;
  description?: string;
  tone?: ToastTone;
  durationMs?: number;
};

type ToastRecord = ToastNotification & {
  id: string;
};

type ToastNotificationsContextValue = {
  notify: (notification: ToastNotification) => string;
  dismiss: (id: string) => void;
};

const ToastNotificationsContext = createContext<ToastNotificationsContextValue | null>(null);

export function ToastNotificationsProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<ToastRecord[]>([]);
  const bodyPortalTarget = typeof document !== "undefined" ? document.body : null;
  const dialogAnnouncerTarget = typeof document !== "undefined" ? document.querySelector<HTMLElement>('[data-slot="dialog-content"]') : null;

  const dismiss = useCallback((id: string) => {
    setToasts((current) => current.filter((toast) => toast.id !== id));
  }, []);

  const notify = useCallback((notification: ToastNotification) => {
    const id = `toast-${Date.now()}-${Math.random().toString(36).slice(2)}`;
    const nextToast: ToastRecord = { ...notification, tone: notification.tone || "default", id };
    setToasts((current) => [...current, nextToast].slice(-MAX_VISIBLE_TOASTS));
    return id;
  }, []);

  const value = useMemo(() => ({ notify, dismiss }), [dismiss, notify]);

  return (
    <ToastNotificationsContext.Provider value={value}>
      <ToastProvider>
        {children}
        {bodyPortalTarget
          ? createPortal(
              <ToastViewport>
                {toasts.map((toast) => (
                  <ToastNotificationItem
                    key={toast.id}
                    toast={toast}
                    dismiss={dismiss}
                    exposeRole={!dialogAnnouncerTarget}
                  />
                ))}
              </ToastViewport>,
              bodyPortalTarget,
            )
          : null}
        {dialogAnnouncerTarget
          ? createPortal(
              <div className="sr-only">
                {toasts.map((toast) => (
                  <div key={toast.id} role={toast.tone === "error" ? "alert" : "status"} aria-label={toast.title}>
                    {toast.title}
                    {toast.description ? ` ${toast.description}` : ""}
                  </div>
                ))}
              </div>,
              dialogAnnouncerTarget,
            )
          : null}
      </ToastProvider>
    </ToastNotificationsContext.Provider>
  );
}

function ToastNotificationItem({
  toast,
  dismiss,
  exposeRole,
}: {
  toast: ToastRecord;
  dismiss: (id: string) => void;
  exposeRole: boolean;
}) {
  useEffect(() => {
    const timeout = window.setTimeout(() => dismiss(toast.id), toast.durationMs ?? 4000);
    return () => window.clearTimeout(timeout);
  }, [dismiss, toast.durationMs, toast.id]);

  return (
    <Toast
      role={exposeRole ? (toast.tone === "error" ? "alert" : "status") : "presentation"}
      aria-label={exposeRole ? toast.title : undefined}
      data-state="open"
      className={toastToneClassName(toast.tone)}
    >
      <div>
        <ToastTitle>{toast.title}</ToastTitle>
        {toast.description ? <ToastDescription>{toast.description}</ToastDescription> : null}
      </div>
      <ToastClose aria-label="Close notification" onClick={() => dismiss(toast.id)} />
    </Toast>
  );
}

export function useToastNotifications() {
  const context = useContext(ToastNotificationsContext);
  if (!context) {
    throw new Error("useToastNotifications must be used within ToastNotificationsProvider.");
  }
  return context;
}

export function toastToneClassName(tone: ToastTone | undefined) {
  if (tone === "success") {
    return "border-[color-mix(in_srgb,var(--success-foreground)_36%,var(--success-background))] bg-[var(--success-background)] text-[var(--success-foreground)]";
  }
  if (tone === "error") {
    return "border-[color-mix(in_srgb,var(--danger-foreground)_36%,var(--danger-background))] bg-[var(--danger-background)] text-[var(--danger-foreground)]";
  }
  if (tone === "warning") {
    return "border-[color-mix(in_srgb,var(--warning-foreground)_36%,var(--warning-background))] bg-[var(--warning-background)] text-[var(--warning-foreground)]";
  }
  if (tone === "info") {
    return "border-primary/30 bg-accent text-accent-foreground";
  }
  return "";
}

export { MAX_VISIBLE_TOASTS };
