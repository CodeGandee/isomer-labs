import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

vi.mock("sigma", () => ({
  default: class {
    on() {}
    kill() {}
  },
}));

import { GraphFiltersBar } from "./features/graph/GraphPanels";

describe("GraphFiltersBar", () => {
  it("labels secondary graph material as supporting records", () => {
    const onChange = vi.fn();
    render(<GraphFiltersBar filters={{ includeSecondary: false }} onChange={onChange} />);

    const checkbox = screen.getByRole("checkbox", { name: "Show supporting records" });
    expect(checkbox.getAttribute("aria-checked")).toBe("false");
    expect(screen.getByText("Supporting Records")).toBeTruthy();

    fireEvent.click(checkbox);

    expect(onChange).toHaveBeenCalledWith({ includeSecondary: true });
  });
});
