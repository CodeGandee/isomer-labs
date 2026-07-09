import * as React from "react"
import { XIcon } from "lucide-react"

import { cn } from "@/lib/utils"

function ToastProvider({
  children,
}: {
  children?: React.ReactNode
}) {
  return <>{children}</>
}

function ToastViewport({
  className,
  ...props
}: React.ComponentProps<"ol">) {
  return (
    <ol
      data-slot="toast-viewport"
      role="region"
      aria-label="Notifications"
      className={cn(
        "fixed right-[max(12px,var(--safe-area-right))] bottom-[max(12px,var(--safe-area-bottom))] z-[60] flex max-h-[min(520px,calc(100dvh-24px))] w-[min(380px,calc(100vw-24px))] list-none flex-col gap-2 outline-none pointer-events-none",
        className
      )}
      {...props}
    />
  )
}

function Toast({
  className,
  ...props
}: React.ComponentProps<"li">) {
  return (
    <li
      data-slot="toast"
      className={cn(
        "pointer-events-auto grid grid-cols-[1fr_auto] items-start gap-3 rounded-md border bg-popover px-4 py-3 text-popover-foreground shadow-lg outline-none data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:animate-in data-[state=open]:fade-in-0 data-[state=closed]:slide-out-to-right-full data-[state=open]:slide-in-from-right-full",
        className
      )}
      {...props}
    />
  )
}

function ToastTitle({
  className,
  ...props
}: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="toast-title"
      className={cn("text-sm font-semibold leading-snug", className)}
      {...props}
    />
  )
}

function ToastDescription({
  className,
  ...props
}: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="toast-description"
      className={cn("mt-1 text-sm leading-snug text-muted-foreground", className)}
      {...props}
    />
  )
}

function ToastClose({
  className,
  ...props
}: React.ComponentProps<"button">) {
  return (
    <button
      type="button"
      data-slot="toast-close"
      className={cn(
        "rounded-md p-1 text-muted-foreground opacity-80 transition-opacity hover:opacity-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
        className
      )}
      {...props}
    >
      <XIcon aria-hidden="true" className="size-4" />
      <span className="sr-only">Close notification</span>
    </button>
  )
}

export {
  Toast,
  ToastClose,
  ToastDescription,
  ToastProvider,
  ToastTitle,
  ToastViewport,
}
