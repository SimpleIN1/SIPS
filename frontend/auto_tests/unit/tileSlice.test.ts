import { describe, expect, it } from "vitest";
import tileReducer, {
  removeTimes,
  setComposite,
  setDotDate,
  setNonDotDate,
  setSatellite,
  setTime,
} from "@/store/tile/tile-slice";
import { ESatellite } from "@/enums/ESatellite";
import { EComposite } from "@/enums/EComposite";

describe("tile slice", () => {
  it("stores selected date in dotted and non-dotted formats", () => {
    const state = tileReducer(undefined, setDotDate("2026-05-14"));

    expect(state.dateTime.dotdate).toBe("2026-05-14");
    expect(state.dateTime.nondotdate).toBe("20260514");
  });

  it("stores selected non-dotted date directly", () => {
    const state = tileReducer(undefined, setNonDotDate("20260515"));

    expect(state.dateTime.nondotdate).toBe("20260515");
  });

  it("stores selected satellite, time and composite", () => {
    let state = tileReducer(undefined, setSatellite(ESatellite.NOAA_20));

    state = tileReducer(state, setTime("0910"));
    state = tileReducer(state, setComposite(EComposite.vievi));

    expect(state.satellite).toBe(ESatellite.NOAA_20);
    expect(state.dateTime.time).toBe("0910");
    expect(state.composite).toBe(EComposite.vievi);
  });

  it("clears available time marks", () => {
    const state = tileReducer(undefined, removeTimes());

    expect(state.times).toEqual([]);
  });
});
