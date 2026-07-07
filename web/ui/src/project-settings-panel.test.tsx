import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import type React from "react";
import { beforeEach, describe, expect, it, vi } from "vitest";

const themeMock = vi.hoisted(() => ({
  setThemeMode: vi.fn(),
}));

vi.mock("sigma", () => ({
  default: class {
    on() {}
    kill() {}
  },
}));

vi.mock("./theme-provider", () => ({
  ThemeProvider: ({ children }: { children: unknown }) => children,
  useGuiTheme: () => ({
    themeMode: "system",
    resolvedThemeMode: "light",
    setThemeMode: themeMock.setThemeMode,
  }),
}));

vi.mock("@/components/ui/select", () => {
  type SelectProps = {
    value?: string;
    onValueChange?: (value: string) => void;
    children?: React.ReactNode;
  };
  type SelectItemProps = {
    value: string;
    children?: React.ReactNode;
  };
  type SelectContainerProps = {
    children?: React.ReactNode;
  };
  return {
    Select: ({ children, onValueChange, value }: SelectProps) => (
      <select aria-label="Global Theme" value={value} onChange={(event: React.ChangeEvent<HTMLSelectElement>) => onValueChange?.(event.target.value)}>
        {children}
      </select>
    ),
    SelectContent: ({ children }: SelectContainerProps) => <>{children}</>,
    SelectItem: ({ children, value }: SelectItemProps) => <option value={value}>{children}</option>,
    SelectTrigger: ({ children }: SelectContainerProps) => <>{children}</>,
    SelectValue: () => null,
  };
});

import { ProjectSettingsPanel } from "./App";

describe("ProjectSettingsPanel", () => {
  beforeEach(() => {
    themeMock.setThemeMode.mockReset();
  });

  it("renders appearance settings and updates the global theme mode", async () => {
    render(<ProjectSettingsPanel />);

    expect(screen.getByRole("heading", { name: "Project Settings" })).toBeTruthy();
    expect(screen.getByText("Resolved theme: light")).toBeTruthy();

    fireEvent.change(screen.getByRole("combobox", { name: "Global Theme" }), { target: { value: "dark" } });

    await waitFor(() => expect(themeMock.setThemeMode).toHaveBeenCalledWith("dark"));
  });
});
