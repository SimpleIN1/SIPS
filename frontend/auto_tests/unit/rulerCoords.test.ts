import { describe, expect, it, vi } from "vitest";
import cursorReducer, {
  changeCursorActive,
  setMousePos,
} from "@/store/cursor/cursor-slice";
import rulerReducer, {
  addRulerMarker,
  addRulerMarkerPos,
  changeIsRulerActive,
  removeRulerMarkers,
} from "@/store/ruler/ruler-slice";
import { convertCoords } from "@/utils/coords";
import { RulerCalculations } from "@/utils/RulerCalculations";

describe("ruler and coordinates", () => {
  it("converts decimal coordinates to degrees, minutes and seconds", () => {
    expect(convertCoords(55.75)).toBe(`55\u00B045'0"`);
    expect(convertCoords(-37.5)).toBe(`37\u00B030'0"`);
  });

  it("stores cursor map position", () => {
    let state = cursorReducer(undefined, changeCursorActive());

    state = cursorReducer(
      state,
      setMousePos({
        lat: 55.75,
        lng: 37.5,
      })
    );

    expect(state.isActive).toBe(true);
    expect(state.mousePos).toEqual({
      lat: 55.75,
      lng: 37.5,
    });
  });

  it("stores and clears ruler points", () => {
    let state = rulerReducer(undefined, changeIsRulerActive());

    state = rulerReducer(state, addRulerMarker([55.75, 37.5]));
    state = rulerReducer(state, addRulerMarkerPos({ x: 100, y: 200 }));

    expect(state.isRulerActive).toBe(true);
    expect(state.rulerMarkers).toEqual([[55.75, 37.5]]);
    expect(state.rulerMarkersPos).toEqual([{ x: 100, y: 200 }]);

    state = rulerReducer(state, removeRulerMarkers());

    expect(state.rulerMarkers).toEqual([]);
    expect(state.rulerMarkersPos).toEqual([]);
  });

  it("calculates midpoint and zero distance between equal points", () => {
    vi.spyOn(console, "log").mockImplementation(() => undefined);

    expect(RulerCalculations.getMidpointSegment([0, 0], [2, 4])).toEqual([
      1,
      2,
    ]);

    expect(RulerCalculations.getLengthSegment([0, 0], [0, 0])).toBe("0 m");
  });
});
