import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { MAX_VISIBLE_TOASTS, ToastNotificationsProvider, useToastNotifications } from "./toast-notifications";

describe("Toast notifications", () => {
  afterEach(() => {
    vi.useRealTimers();
    cleanup();
  });

  it("renders and dismisses transient notifications without moving focus", async () => {
    render(
      <ToastNotificationsProvider>
        <NotifyButton />
      </ToastNotificationsProvider>,
    );

    const button = screen.getByRole("button", { name: "Notify" });
    button.focus();
    fireEvent.click(button);

    expect(await screen.findByRole("status", { name: "Saved." })).toBeTruthy();
    expect(document.activeElement).toBe(button);

    fireEvent.click(screen.getByRole("button", { name: "Close notification" }));
    await waitFor(() => expect(screen.queryByText("Saved.")).toBeNull());
  });

  it("keeps no more than five toast notifications visible", async () => {
    render(
      <ToastNotificationsProvider>
        <BurstButton />
      </ToastNotificationsProvider>,
    );

    fireEvent.click(screen.getByRole("button", { name: "Burst" }));

    await waitFor(() => expect(screen.getAllByRole("status")).toHaveLength(MAX_VISIBLE_TOASTS));
    expect(screen.queryByText("Toast 1")).toBeNull();
    expect(screen.getByText("Toast 2")).toBeTruthy();
    expect(screen.getByText("Toast 6")).toBeTruthy();
  });

  it("dismisses notifications after their configured timeout", async () => {
    vi.useFakeTimers();
    render(
      <ToastNotificationsProvider>
        <ShortToastButton />
      </ToastNotificationsProvider>,
    );

    fireEvent.click(screen.getByRole("button", { name: "Short" }));
    expect(screen.getByRole("status", { name: "Short lived." })).toBeTruthy();

    act(() => {
      vi.advanceTimersByTime(399);
    });
    expect(screen.getByText("Short lived.")).toBeTruthy();

    act(() => {
      vi.advanceTimersByTime(1);
    });
    expect(screen.queryByText("Short lived.")).toBeNull();
  });

  it("uses alert semantics for error notifications", async () => {
    render(
      <ToastNotificationsProvider>
        <ErrorButton />
      </ToastNotificationsProvider>,
    );

    fireEvent.click(screen.getByRole("button", { name: "Error" }));
    expect(await screen.findByRole("alert", { name: "Copy failed." })).toBeTruthy();
  });
});

function NotifyButton() {
  const { notify } = useToastNotifications();
  return (
    <button type="button" onClick={() => notify({ title: "Saved.", tone: "success", durationMs: 10000 })}>
      Notify
    </button>
  );
}

function BurstButton() {
  const { notify } = useToastNotifications();
  return (
    <button
      type="button"
      onClick={() => {
        for (let index = 1; index <= MAX_VISIBLE_TOASTS + 1; index += 1) {
          notify({ title: `Toast ${index}`, tone: "info", durationMs: 10000 });
        }
      }}
    >
      Burst
    </button>
  );
}

function ErrorButton() {
  const { notify } = useToastNotifications();
  return (
    <button type="button" onClick={() => notify({ title: "Copy failed.", tone: "error", durationMs: 10000 })}>
      Error
    </button>
  );
}

function ShortToastButton() {
  const { notify } = useToastNotifications();
  return (
    <button type="button" onClick={() => notify({ title: "Short lived.", tone: "info", durationMs: 400 })}>
      Short
    </button>
  );
}
